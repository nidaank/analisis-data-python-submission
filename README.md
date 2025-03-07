# Dicoding Collection Dashboard

Dashboard ini dikembangkan menggunakan **Streamlit** untuk menampilkan hasil analisis data secara interaktif.

## 📌 Persyaratan
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal **Python 3.9 atau versi lebih baru** dan memiliki **pip** atau **conda** yang terinstal di sistem Anda.

## ⚙️ Setup Environment

### 🔹 Menggunakan Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### 🔹 Menggunakan Shell/Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 🚀 Menjalankan Dashboard Streamlit
1. **Pastikan dependensi sudah terpasang**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan aplikasi Streamlit**
   ```bash
   streamlit run dashboard.py
   ```

Dashboard akan berjalan di **localhost** dan dapat diakses melalui browser pada **http://localhost:8501/**.

## 📊 Menjalankan Jupyter Notebook (Opsional)
Jika proyek ini memiliki file **notebook.ipynb**, Anda bisa menjalankan analisis data menggunakan **Jupyter Notebook**:
```bash
pip install -r requirements.txt
jupyter notebook notebook.ipynb
```
