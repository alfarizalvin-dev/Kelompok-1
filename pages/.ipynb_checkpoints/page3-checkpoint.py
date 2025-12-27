import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import altair as alt



# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Analisis Data & Kesimpulan",
    layout="wide"
)

# =====================================================
# STYLE (UI COLORFULL)
# =====================================================
st.markdown("""
<style>
.main { background-color: #f8fafc; }
h1 { color: #1e40af; }
h2 { color: #0f766e; }
.metric-box {
    background-color: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    text-align: center;
}
.highlight {
    background-color: #ecfeff;
    padding: 18px;
    border-left: 6px solid #06b6d4;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "Dataset_prakbigdata.xlsx")
GEO_PATH = os.path.join(BASE_DIR, "indonesia_provinsi.json")

df = pd.read_excel(DATA_PATH)

# =====================================================
# STANDARISASI KOLOM
# =====================================================
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("%", "")
)

kol_prov = df.columns[0]
kol_tahun = df.columns[1]
indikator = df.columns[2:]

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("🔍 Filter Data")

provinsi_list = sorted(df[kol_prov].unique())

provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    provinsi_list,
    default=provinsi_list
)

tahun = st.sidebar.slider(
    "Rentang Tahun",
    int(df[kol_tahun].min()),
    int(df[kol_tahun].max()),
    (int(df[kol_tahun].min()), int(df[kol_tahun].max()))
)

indikator_pilihan = st.sidebar.selectbox(
    "Pilih Indikator",
    indikator
)

filtered_df = df[
    (df[kol_prov].isin(provinsi)) &
    (df[kol_tahun].between(tahun[0], tahun[1]))
]

# =====================================================
# TITLE
# =====================================================
st.title("📊 Analisis Data & Kesimpulan Dinamis")

st.markdown("""
Halaman ini menyajikan **analisis interaktif** berbasis data pembangunan provinsi.
Seluruh grafik, peta, dan kesimpulan akan **berubah otomatis** sesuai filter.
""")

# =====================================================
# METRIC RINGKASAN
# =====================================================
st.subheader("📌 Ringkasan Statistik")

mean_values = filtered_df[indikator].mean()

cols = st.columns(4)
for i, col in enumerate(mean_values.index):
    with cols[i % 4]:
        st.markdown(
            f"""
            <div class="metric-box">
                <b>{col.replace('_',' ').upper()}</b><br>
                <h3>{mean_values[col]:.2f}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================================
# BAR & LINE SIDE BY SIDE
# =====================================================
st.subheader("📊 Perbandingan & Tren Indikator")

col1, col2 = st.columns(2)

# ---------- BAR ----------
prov_df = (
    filtered_df
    .groupby(kol_prov)[indikator_pilihan]
    .mean()
    .reset_index()
    .sort_values(by=indikator_pilihan)
)

bar_chart = alt.Chart(prov_df).mark_bar().encode(
    y=alt.Y(f"{kol_prov}:N", title="Provinsi"),
    x=alt.X(f"{indikator_pilihan}:Q", title="Rata-rata"),
    color=alt.Color(f"{kol_prov}:N", legend=None),
    tooltip=[kol_prov, indikator_pilihan]
)

with col1:
    st.altair_chart(bar_chart, use_container_width=True)

# ---------- LINE ----------
trend_df = (
    filtered_df
    .groupby([kol_tahun, kol_prov])[indikator_pilihan]
    .mean()
    .reset_index()
)

line_chart = alt.Chart(trend_df).mark_line(point=True).encode(
    x=alt.X(f"{kol_tahun}:O", title="Tahun"),
    y=alt.Y(f"{indikator_pilihan}:Q", title="Nilai"),
    color=alt.Color(f"{kol_prov}:N", title="Provinsi"),
    tooltip=[kol_prov, kol_tahun, indikator_pilihan]
)

with col2:
    st.altair_chart(line_chart, use_container_width=True)


# =====================================================
# ANALISIS PARAGRAF OTOMATIS
# =====================================================
st.subheader("🧠 Analisis Data")

analisis = []
for col in indikator:
    tren = filtered_df.groupby(kol_tahun)[col].mean()
    if len(tren) > 1:
        arah = "meningkat 📈" if tren.iloc[-1] > tren.iloc[0] else "menurun 📉"
        analisis.append(
            f"Rata-rata {col.replace('_',' ').upper()} sebesar {mean_values[col]:.2f} "
            f"dan secara umum {arah} selama periode pengamatan."
        )

st.markdown(
    "<div class='highlight'>" + " ".join(analisis) + "</div>",
    unsafe_allow_html=True
)

# =====================================================
# DOWNLOAD DATA
# =====================================================
st.subheader("📥 Unduh Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Data Terfilter (CSV)",
    csv,
    "data_page3_terfilter.csv",
    "text/csv"
)

# =====================================================
# PREVIEW
# =====================================================
with st.expander("📋 Lihat Data Terfilter"):
    st.dataframe(filtered_df)

# =====================================================
# FILTER & ANALISIS SEBAB-AKIBAT INTERAKTIF
# =====================================================
st.subheader("🧩 Analisis Sebab-Akibat (Tabel Interaktif)")

# Sidebar filter khusus sebab-akibat
st.sidebar.markdown("### 🔹 Filter Sebab-Akibat")
indikator_sebab = st.sidebar.multiselect(
    "Pilih Indikator Penyebab",
    indikator,
    default=indikator
)

indikator_dampak = st.sidebar.multiselect(
    "Pilih Indikator Dampak",
    indikator,
    default=indikator
)

# Buat list untuk menampung hasil
sebab_akibat_data = []

for col1 in indikator_sebab:
    tren1 = filtered_df.groupby(kol_tahun)[col1].mean()
    if len(tren1) < 2:
        continue
    arah1 = "Meningkat 📈" if tren1.iloc[-1] > tren1.iloc[0] else "Menurun 📉"
    
    for col2 in indikator_dampak:
        if col1 == col2:
            continue  # jangan bandingkan dengan dirinya sendiri
        tren2 = filtered_df.groupby(kol_tahun)[col2].mean()
        if len(tren2) < 2:
            continue
        arah2 = "Meningkat 📈" if tren2.iloc[-1] > tren2.iloc[0] else "Menurun 📉"

        pengaruh = "Positif ✅" if arah1 == arah2 else "Negatif ❌"

        sebab_akibat_data.append({
            "Indikator Penyebab": col1.replace("_"," ").title(),
            "Indikator Dampak": col2.replace("_"," ").title(),
            "Arah Penyebab": arah1,
            "Arah Dampak": arah2,
            "Pengaruh": pengaruh
        })

# Tampilkan tabel
if sebab_akibat_data:
    df_sebab_akibat = pd.DataFrame(sebab_akibat_data)
    st.dataframe(df_sebab_akibat)
else:
    st.write("Tidak ada data untuk kombinasi indikator yang dipilih.")
