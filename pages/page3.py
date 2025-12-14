import streamlit as st
import pandas as pd
import os
import numpy as np

st.markdown("""
<style>
/* Background utama */
.main {
    background-color: #f8fafc;
}

/* Judul */
h1 {
    color: #1e3a8a;
}

/* Subjudul */
h2, h3 {
    color: #0f766e;
}

/* Box metrik */
.metric-container {
    background-color: #ffffff;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Highlight kesimpulan */
.highlight {
    background-color: #ecfeff;
    padding: 15px;
    border-left: 6px solid #06b6d4;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Analisis & Kesimpulan", layout="wide")

# ===============================
# LOAD DATASET
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Dataset_prakbigdata.xlsx")

df = pd.read_excel(DATA_PATH)

# ===============================
# STANDARISASI NAMA KOLOM
# ===============================
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("%", "")
)

# ===============================
# IDENTIFIKASI KOLOM UTAMA
# (AMAN UNTUK DATASET BERBEDA)
# ===============================
kol_prov = df.columns[0]
kol_tahun = df.columns[1]

indikator = df.columns[2:]  # sisanya indikator pembangunan

# ===============================
# JUDUL
# ===============================
st.title("📊 Analisis dan Kesimpulan")

st.markdown("""
Halaman ini menyajikan **analisis empiris dan kesimpulan berbasis data**  
yang **berubah secara otomatis** sesuai dengan wilayah dan periode waktu yang dipilih.
""")

# ===============================
# FILTER
# ===============================
st.sidebar.header("🔍 Filter Data")

provinsi = st.sidebar.multiselect(
    "Pilih Wilayah",
    options=sorted(df[kol_prov].unique()),
    default=sorted(df[kol_prov].unique())
)

tahun = st.sidebar.slider(
    "Rentang Tahun",
    int(df[kol_tahun].min()),
    int(df[kol_tahun].max()),
    (int(df[kol_tahun].min()), int(df[kol_tahun].max()))
)

filtered_df = df[
    (df[kol_prov].isin(provinsi)) &
    (df[kol_tahun].between(tahun[0], tahun[1]))
]

# ===============================
# RINGKASAN STATISTIK
# ===============================
mean_values = filtered_df[indikator].mean()


st.subheader("📈 Ringkasan Statistik Utama")

cols = st.columns(3)
for i, col in enumerate(mean_values.index):
    with cols[i % 3]:
        st.metric(
            label=col.replace("_", " ").upper(),
            value=f"{mean_values[col]:.2f}"
        )

st.subheader("📊 Tren Indikator")

selected_indicator = st.selectbox(
    "Pilih indikator untuk ditampilkan",
    indikator
)

trend_df = (
    filtered_df
    .groupby(kol_tahun)[selected_indicator]
    .mean()
    .reset_index()
)

st.line_chart(
    trend_df.set_index(kol_tahun)
)


st.markdown("### ⬇️ Unduh Data yang Ditampilkan")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download data (CSV)",
    data=csv,
    file_name="data_terfilter_page3.csv",
    mime="text/csv"
)


# ===============================
# ANALISIS OTOMATIS
# ===============================
st.subheader("🔎 Analisis Data")

analisis_teks = []

for col in indikator:
    nilai = mean_values[col]
    tren = filtered_df.groupby(kol_tahun)[col].mean()

    if tren.iloc[-1] > tren.iloc[0]:
        arah = "mengalami peningkatan"
    else:
        arah = "mengalami penurunan"

    analisis_teks.append(
        f"- Rata-rata **{col.replace('_', ' ').upper()}** sebesar **{nilai:.2f}** "
        f"dan secara umum **{arah}** pada periode pengamatan."
    )

for a in analisis_teks:
    st.markdown(a)

# ===============================
# KESIMPULAN DINAMIS
# ===============================
st.subheader("✅ Kesimpulan")

st.markdown(f"""
<div class="highlight">
<b>Kesimpulan Utama:</b><br><br>
Berdasarkan data wilayah <b>{', '.join(provinsi)}</b> pada periode
<b>{tahun[0]}–{tahun[1]}</b>, indikator pembangunan menunjukkan dinamika
yang saling berkaitan dan mencerminkan kondisi ekonomi serta sosial daerah.

Perubahan indikator mengindikasikan bahwa kebijakan pembangunan perlu
dirancang secara terintegrasi agar pertumbuhan yang dicapai bersifat
inklusif dan berkelanjutan.
</div>
""", unsafe_allow_html=True)


# ===============================
# DATA PREVIEW (OPSIONAL)
# ===============================
with st.expander("📋 Lihat Data Terfilter"):
    st.dataframe(filtered_df)


# ======================================================
# INTERPRETASI SEBAB–AKIBAT
# ======================================================
st.subheader("🔍 Interpretasi Sebab–Akibat")

for col in indikator:
    with st.expander(f"Analisis {col.replace('_',' ').upper()}"):
        tren = filtered_df.groupby(kol_tahun)[col].mean()
        arah = "meningkat" if tren.iloc[-1] > tren.iloc[0] else "menurun"

        st.markdown(
            f"📌 **Tren:** {arah.capitalize()} selama periode pengamatan.\n\n"
        )

        if "ipm" in col:
            st.info(
                "Peningkatan IPM menunjukkan perbaikan kualitas sumber daya manusia "
                "yang berpotensi mendorong produktivitas dan pertumbuhan ekonomi."
            )
        elif "tpt" in col:
            st.warning(
                "Perubahan tingkat pengangguran mencerminkan kondisi pasar tenaga kerja "
                "yang berdampak langsung pada kesejahteraan masyarakat."
            )
        elif "miskin" in col:
            st.success(
                "Penurunan tingkat kemiskinan mengindikasikan dampak positif kebijakan "
                "dan pertumbuhan ekonomi terhadap kesejahteraan."
            )
        elif "gini" in col:
            st.error(
                "Ketimpangan yang meningkat berpotensi mengurangi inklusivitas pertumbuhan."
            )
