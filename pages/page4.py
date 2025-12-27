import streamlit as st
from PIL import Image
from pathlib import Path

# =========================
# PATH AMAN (WAJIB)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

img1_path = BASE_DIR / "bps1.jpeg"
img2_path = BASE_DIR / "bps2.jpeg"
img3_path = BASE_DIR / "bps3.jpeg"

# =========================
# KONTEN
# =========================
st.title("⬇️ Cara Mengunduh Dataset dari Website BPS")
st.markdown("---")

st.write(
    "Halaman ini menjelaskan tahapan pengunduhan dataset resmi dari "
    "**Badan Pusat Statistik (BPS)**."
)

# =========================
# GAMBAR 1
# =========================
st.subheader("1️⃣ Tampilan Awal Website BPS")
st.image(
    Image.open(img1_path),
    caption="Pada tampilan awal website resmi Badan Pusat Statistik (BPS), klik produk kemudian klik Tabel Dinamis",
    use_container_width=True
)

st.write("Akses website resmi BPS melalui **https://www.bps.go.id**.")

# =========================
# GAMBAR 2
# =========================
st.subheader("2️⃣ Memasukkan Filter Data")
st.image(
    Image.open(img2_path),
    caption="Pemilihan subjek, indikator, filter wilayah, periode, atau variabel data sesuai kebutuhan",
    use_container_width=True
)

st.write("Gunakan filter untuk menentukan wilayah dan periode data.")

# =========================
# GAMBAR 3
# =========================
st.subheader("3️⃣ Mengunduh Dataset")
st.image(
    Image.open(img3_path),
    caption="Tombol hujau untuk unduh dataset dari website BPS",
    use_container_width=True
)

st.write("Klik tombol **Unduh** dan pilih format file yang diinginkan.")

st.markdown("---")
st.success("Dataset BPS siap digunakan untuk analisis.")
