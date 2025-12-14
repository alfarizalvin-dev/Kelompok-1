import streamlit as st

# Judul Utama
st.title("Analisis Pengaruh Indikator Pembangunan Manusia terhadap Pertumbuhan Ekonomi")

st.markdown("---")

# Definisi
st.header("Definisi")

st.write("""
Pembangunan manusia merupakan proses perluasan pilihan bagi penduduk
untuk mencapai kehidupan yang lebih layak. Indikator Pembangunan Manusia
(IPM) digunakan untuk mengukur keberhasilan pembangunan manusia yang
dilihat dari aspek kesehatan, pendidikan, dan standar hidup layak.

Pertumbuhan ekonomi menunjukkan peningkatan kapasitas produksi suatu
perekonomian yang tercermin dari meningkatnya Produk Domestik Bruto (PDB)
atau Produk Domestik Regional Bruto (PDRB) dari waktu ke waktu.
""")

# Gambaran Umum Variabel
st.header("Gambaran Umum Variabel Perekonomian")

st.write("""
Variabel-variabel yang digunakan dalam analisis ini meliputi:

1. **Indeks Pembangunan Manusia (IPM)**  
   Menggambarkan kualitas pembangunan manusia yang dilihat dari tiga
   dimensi utama, yaitu kesehatan, pendidikan, dan standar hidup layak.

2. **Pertumbuhan Ekonomi**  
   Menggambarkan tingkat perkembangan aktivitas ekonomi suatu wilayah
   dalam periode tertentu.

Analisis ini bertujuan untuk melihat sejauh mana indikator pembangunan
manusia berpengaruh terhadap pertumbuhan ekonomi.
""")
