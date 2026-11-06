from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

sns.set_theme(style="whitegrid")

# ==========================================
# 2. MEMUAT DATA
# ==========================================

# Lokasi file dihitung dari lokasi dashboard.py, bukan dari folder
# tempat terminal dijalankan. Ini mencegah FileNotFoundError di VS Code.
BASE_DIR = Path(__file__).resolve().parent


def find_csv(filename):
    """Cari CSV di folder yang sama, atau di folder 'data' / 'dashboard'."""
    candidates = [
        BASE_DIR / filename,
        BASE_DIR / "data" / filename,
        BASE_DIR / "dashboard" / filename,
        BASE_DIR.parent / "data" / filename,
        BASE_DIR.parent / "dashboard" / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


@st.cache_data
def load_data():
    day_path = find_csv("day_cleaned.csv")
    hour_path = find_csv("hour_cleaned.csv")

    if day_path is None or hour_path is None:
        return None, None

    day = pd.read_csv(day_path)
    hour = pd.read_csv(hour_path)

    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])

    return day, hour


day_df, hour_df = load_data()

if day_df is None or hour_df is None:
    st.error(
        "File day.csv dan/atau hour.csv tidak ditemukan. "
        f"Letakkan keduanya di folder: {BASE_DIR}"
    )
    st.stop()

# ==========================================
# 3. PERSIAPAN DATA
# ==========================================

season_mapping = {
    1: "Semi",
    2: "Panas",
    3: "Gugur",
    4: "Dingin"
}

weather_mapping = {
    1: "Cerah",
    2: "Berkabut / Berawan",
    3: "Salju / Hujan Ringan",
    4: "Hujan Lebat / Salju Lebat"
}

workingday_mapping = {
    0: "Hari Nonkerja",
    1: "Hari Kerja"
}

day_df["season_label"] = day_df["season"].map(season_mapping)
day_df["weather_label"] = day_df["weathersit"].map(weather_mapping)
day_df["workingday_label"] = day_df["workingday"].map(workingday_mapping)

hour_df["workingday_label"] = hour_df["workingday"].map(workingday_mapping)

# ==========================================
# 4. JUDUL DASHBOARD
# ==========================================

st.title("Dashboard Penyewaan Sepeda🚲")

st.write(
    "Dashboard analisis penyewaan sepeda berdasarkan "
    "hari kerja, musim, kondisi cuaca, dan jam penyewaan "
    "selama periode 2011–2012."
)

st.divider()

# ==========================================
# 5. SIDEBAR DAN FILTER
# ==========================================

# Gambar sepeda di tengah
st.sidebar.markdown(
    """
    <div style="text-align:center;">
        <img src="https://img.icons8.com/color/96/000000/bicycle.png"
             width="130"
             style="display:block; margin:0 auto 10px auto;">
        <h2 style="margin:0 0 4px 0;">Jelajah Data</h2>
        <p style="opacity:0.8; font-size:0.9rem;">
            Pilih analisis dan rentang tanggal untuk melihat
            informasi penyewaan sepeda.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.divider()

# Nama pilihan dibuat konstanta supaya SAMA PERSIS dengan kondisi if/elif
# di bawah (sebelumnya berbeda sehingga halaman kosong).
OPT_1 = "Hari Kerja vs Nonkerja"
OPT_2 = "Musim dan Cuaca"
OPT_3 = "Pola Penyewaan per Jam"
OPT_4 = "Korelasi"

analysis_choice = st.sidebar.selectbox(
    "Pilih Analisis",
    [OPT_1, OPT_2, OPT_3, OPT_4]
)

st.sidebar.subheader("Filter Tanggal")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

start_date = st.sidebar.date_input(
    "Tanggal Awal",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "Tanggal Akhir",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

if start_date > end_date:
    st.error("Tanggal awal tidak boleh melebihi tanggal akhir.")
    st.stop()

# Filter data harian
filtered_day = day_df[
    (day_df["dteday"].dt.date >= start_date) &
    (day_df["dteday"].dt.date <= end_date)
].copy()

# Filter data per jam
filtered_hour = hour_df[
    (hour_df["dteday"].dt.date >= start_date) &
    (hour_df["dteday"].dt.date <= end_date)
].copy()

if filtered_day.empty:
    st.warning("Tidak terdapat data pada rentang tanggal tersebut.")
    st.stop()

# ==========================================
# 6. METRIK UTAMA
# ==========================================

total_rentals = filtered_day["cnt"].sum()
total_registered = filtered_day["registered"].sum()
total_casual = filtered_day["casual"].sum()
average_daily = filtered_day["cnt"].mean()

def format_id(angka):
    """Format angka gaya Indonesia: 3299267 -> 3.299.267"""
    return f"{angka:,.0f}".replace(",", ".")


def metric_card(label, value, bg, label_color, value_color):
    return f"""
    <div style="background-color:{bg}; border:1px solid rgba(0,0,0,0.06);
                border-radius:14px; padding:18px 22px;">
        <div style="color:{label_color}; font-size:0.95rem;
                    font-weight:600; margin-bottom:6px;">
            {label}
        </div>
        <div style="color:{value_color}; font-size:2.1rem;
                    font-weight:700; line-height:1.2;">
            {value}
        </div>
    </div>
    """


cards_html = "".join([
    metric_card("🚲 Total Penyewaan", format_id(total_rentals),
                "#E3F0FA", "#2F6B9A", "#25507A"),
    metric_card("👥 Pengguna Terdaftar", format_id(total_registered),
                "#E3F2E8", "#3C7A52", "#2E5E40"),
    metric_card("🧍 Pengguna Kasual", format_id(total_casual),
                "#FFF0DF", "#C9772B", "#8A5524"),
    metric_card("📊 Rata-rata Harian", format_id(average_daily),
                "#F1EAF8", "#7A5AA6", "#5E4390"),
])

# Susunan 2 x 2, warna label dan angka mengikuti warna kartu.
st.markdown(
    f"""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        {cards_html}
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# 7. PERTANYAAN 1
# ==========================================

if analysis_choice == OPT_1:

    st.header("Hari Kerja vs Hari Nonkerja")

    st.write(
        "Bagaimana perbedaan rata-rata jumlah penyewaan "
        "sepeda antara hari kerja dan hari nonkerja?"
    )

    workingday_avg = (
        filtered_day.groupby("workingday_label")["cnt"]
        .mean()
        .reindex(["Hari Kerja", "Hari Nonkerja"])
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(
        workingday_avg.index,
        workingday_avg.values,
        color=["#6A9FB5", "#E6A66A"][:len(workingday_avg)],
        width=0.55
    )

    ax.set_title(
        "Rata-rata Penyewaan Berdasarkan Jenis Hari",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Jenis Hari")
    ax.set_ylabel("Rata-rata Penyewaan")

    ax.bar_label(
        bars,
        labels=[f"{x:,.0f}" for x in workingday_avg.values],
        padding=4
    )

    ax.set_ylim(0, workingday_avg.max() * 1.2)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    if len(workingday_avg) == 2:
        difference = (
            workingday_avg["Hari Kerja"] -
            workingday_avg["Hari Nonkerja"]
        )

        st.info(
            f"Selisih rata-rata penyewaan antara hari kerja "
            f"dan hari nonkerja adalah {abs(difference):,.0f} penyewaan."
        )

# ==========================================
# 8. PERTANYAAN 2
# ==========================================

elif analysis_choice == OPT_2:

    st.header("Penyewaan Berdasarkan Musim dan Cuaca")

    st.write(
        "Bagaimana perbedaan rata-rata jumlah penyewaan "
        "sepeda berdasarkan musim dan kondisi cuaca?"
    )

    col_a, col_b = st.columns(2)

    # Grafik musim
    with col_a:

        season_avg = (
            filtered_day.groupby("season_label")["cnt"]
            .mean()
            .reindex(["Semi", "Panas", "Gugur", "Dingin"])
            .dropna()
        )

        fig, ax = plt.subplots(figsize=(7, 5))

        bars = ax.bar(
            season_avg.index,
            season_avg.values,
            color=["#A8C5A0", "#E9C46A", "#E69A73", "#8FA8C8"][:len(season_avg)]
        )

        ax.set_title("Rata-rata Penyewaan Berdasarkan Musim", fontweight="bold")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Penyewaan")

        ax.bar_label(
            bars,
            labels=[f"{x:,.0f}" for x in season_avg.values],
            padding=3
        )

        ax.set_ylim(0, season_avg.max() * 1.2)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # Grafik cuaca
    with col_b:

        weather_order = [
            "Cerah",
            "Berkabut / Berawan",
            "Salju / Hujan Ringan",
            "Hujan Lebat / Salju Lebat"
        ]
        weather_colors = {
            "Cerah": "#E9C46A",
            "Berkabut / Berawan": "#A8B8C8",
            "Salju / Hujan Ringan": "#7FA6C9",
            "Hujan Lebat / Salju Lebat": "#718096"
        }

        weather_avg = (
            filtered_day.groupby("weather_label")["cnt"]
            .mean()
            .reindex(weather_order)
            .dropna()
        )

        fig, ax = plt.subplots(figsize=(7, 5))

        bars = ax.bar(
            weather_avg.index,
            weather_avg.values,
            color=[weather_colors[w] for w in weather_avg.index]
        )

        ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca", fontweight="bold")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.tick_params(axis="x", rotation=15)

        ax.bar_label(
            bars,
            labels=[f"{x:,.0f}" for x in weather_avg.values],
            padding=3
        )

        ax.set_ylim(0, weather_avg.max() * 1.2)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ==========================================
# 9. PERTANYAAN 3
# ==========================================

elif analysis_choice == OPT_3:

    st.header("Pola Penyewaan Sepeda Berdasarkan Jam")

    st.write(
        "Pada jam berapa jumlah penyewaan sepeda mencapai "
        "puncak dan titik terendah, serta bagaimana "
        "perbedaannya antara hari kerja dan hari nonkerja?"
    )

    hourly_avg = (
        filtered_hour.groupby(["hr", "workingday_label"])["cnt"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    for day_type, color in [
        ("Hari Kerja", "#6A9FB5"),
        ("Hari Nonkerja", "#E6A66A")
    ]:
        subset = hourly_avg[hourly_avg["workingday_label"] == day_type]

        if subset.empty:
            continue

        ax.plot(
            subset["hr"],
            subset["cnt"],
            marker="o",
            linewidth=2,
            label=day_type,
            color=color
        )

    ax.set_title(
        "Rata-rata Penyewaan Sepeda per Jam",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(24))
    ax.legend(title="Jenis Hari")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Jam puncak dan terendah
    col_a, col_b = st.columns(2)

    for day_type, column in [
        ("Hari Kerja", col_a),
        ("Hari Nonkerja", col_b)
    ]:
        subset = hourly_avg[hourly_avg["workingday_label"] == day_type]

        if not subset.empty:
            peak = subset.loc[subset["cnt"].idxmax()]
            lowest = subset.loc[subset["cnt"].idxmin()]

            with column:
                st.subheader(day_type)

                st.metric(
                    "Jam Puncak",
                    f"{int(peak['hr']):02d}:00",
                    f"{peak['cnt']:,.0f} penyewaan",
                    delta_color="off"
                )

                st.metric(
                    "Jam Terendah",
                    f"{int(lowest['hr']):02d}:00",
                    f"{lowest['cnt']:,.0f} penyewaan",
                    delta_color="off"
                )

# ==========================================
# 10. ANALISIS LANJUTAN
# ==========================================

elif analysis_choice == OPT_4:

    st.header("Analisis Korelasi")

    st.write(
        "Analisis korelasi Pearson digunakan untuk melihat "
        "hubungan antara kondisi lingkungan dan jumlah "
        "penyewaan sepeda."
    )

    correlation_cols = ["temp", "atemp", "hum", "windspeed", "cnt"]

    nama_variabel = {
        "temp": "Suhu",
        "atemp": "Suhu Terasa",
        "hum": "Kelembapan",
        "windspeed": "Kecepatan Angin",
        "cnt": "Jumlah Penyewaan"
    }

    correlation_matrix = (
        filtered_day[correlation_cols]
        .corr(method="pearson")
        .rename(index=nama_variabel, columns=nama_variabel)
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        vmin=-1,
        vmax=1,
        center=0,
        ax=ax
    )

    ax.set_title(
        "Heatmap Korelasi Kondisi Lingkungan dan Penyewaan",
        fontweight="bold"
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    cnt_correlation = (
        correlation_matrix["Jumlah Penyewaan"]
        .drop("Jumlah Penyewaan")
        .sort_values(ascending=False)
    )

    st.subheader("Korelasi terhadap Jumlah Penyewaan")

    st.dataframe(
        cnt_correlation.rename("Nilai Korelasi").to_frame(),
        width="stretch"
    )

    st.caption(
        "Korelasi menunjukkan hubungan antarvariabel, "
        "bukan hubungan sebab-akibat."
    )

# ==========================================
# 11. FOOTER
# ==========================================
from datetime import datetime
st.divider()

st.markdown(
    f"""
    <div style="text-align:center; opacity:0.75; font-size:0.85rem;">
        Dataset Penyewaan Sepeda | Periode 2011–2012<br>
        © {datetime.now().year} <b>Musfirah</b>. Hak cipta dilindungi.
    </div>
    """,
    unsafe_allow_html=True
)