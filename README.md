# Bike Sharing Data Analysis

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda menggunakan Bike Sharing Dataset periode 2011–2012.

Analisis dilakukan untuk mengetahui pola penyewaan sepeda berdasarkan hari kerja dan hari nonkerja, musim, kondisi cuaca, serta jam penyewaan. Hasil analisis disajikan melalui notebook dan dashboard interaktif menggunakan Streamlit.

## Struktur Direktori

```text
bike-sharing-dashboard/
├── data/
│   ├── day_cleaned.csv
│   └── hour_cleaned.csv
│
├── dashboard.py
├── Proyek_Analisis_Data.ipynb
├── README.md
└── requirements.txt
```

## Teknologi yang Digunakan

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Instalasi dan Persiapan

Pastikan Python sudah terinstal pada perangkat. Kemudian ikuti langkah-langkah berikut melalui terminal.

**1. Clone repository**

```bash
git clone https://github.com/musfira19/bike-sharing-dashboard.git
```

**2. Masuk ke folder proyek**

```bash
cd bike-sharing-dashboard
```

**3. Buat virtual environment**

```bash
python -m venv venv
```

**4. Aktifkan virtual environment**

Untuk Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

**5. Instal library yang dibutuhkan**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Menjalankan Dashboard

Setelah seluruh library berhasil diinstal, jalankan perintah berikut melalui terminal pada folder proyek:

```bash
python -m streamlit run dashboard.py
```

Setelah perintah dijalankan, Streamlit akan menampilkan alamat lokal pada terminal, biasanya:

```text
http://localhost:8501
```

Buka alamat tersebut melalui browser untuk mengakses dashboard interaktif.

## Dataset

Dataset yang digunakan merupakan Bike Sharing Dataset yang terdiri dari:

- `day_cleaned.csv`: Data penyewaan sepeda harian yang telah melalui proses pembersihan data.
- `hour_cleaned.csv`: Data penyewaan sepeda per jam yang telah melalui proses pembersihan data.

Dataset awal bersumber dari Bike Sharing Dataset (2011–2012).

## Notebook Analisis

Proses analisis data dilakukan melalui notebook `Proyek_Analisis_Data.ipynb`, yang mencakup:

- Data Wrangling
- Exploratory Data Analysis (EDA)
- Data Visualization
- Penyusunan kesimpulan hasil analisis