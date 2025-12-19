import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Analisis Indikator Pembangunan Provinsi")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset.xlsx")
    return df

df = load_data()

# rapikan
df["Provinsi"] = df["Provinsi"].str.strip().str.title()
df["Tahun"] = df["Tahun"].astype(int)

indikator_list = [
    "AHH",                 # Angka Harapan Hidup
    "AML",                 # Angka Melek Huruf
    "PPM",                 # Penduduk Miskin
    "RLS",                 # Rata-rata Lama Sekolah
    "TPT",                 # Tingkat Pengangguran Terbuka
    "IPM",                 # Indeks Pembangunan Manusia
    "E_Growth",            # Pertumbuhan Ekonomi
    "Laju_Pertumbuhan",    # Laju Pertumbuhan (alternatif)
    "PDRB_Kapita",         # PDRB per Kapita
    "Inflasi_(YoY)",       # Inflasi Year-on-Year
    "Gini_Ratio"           # Ketimpangan
]

# =====================
# SIDEBAR FILTER
# =====================
st.sidebar.header("Filter")

indikator = st.sidebar.selectbox(
    "Pilih Indikator",
    indikator_list
)

provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    sorted(df["Provinsi"].unique()),
    default=["Sumatera Utara"]
)

tahun_range = st.sidebar.slider(
    "Rentang Tahun",
    int(df["Tahun"].min()),
    int(df["Tahun"].max()),
    (int(df["Tahun"].min()), int(df["Tahun"].max()))
)

# =====================
# FILTER DATA
# =====================
df_filtered = df[
    (df["Provinsi"].isin(provinsi)) &
    (df["Tahun"].between(tahun_range[0], tahun_range[1]))
]

df_filtered[indikator] = pd.to_numeric(
    df_filtered[indikator], errors="coerce"
)

# =====================
# LINE CHART
# =====================
st.subheader(f"Perkembangan {indikator} Antar Provinsi")

fig = px.line(
    df_filtered,
    x="Tahun",
    y=indikator,
    color="Provinsi",
    markers=True,
    title=f"Tren {indikator} ({tahun_range[0]}–{tahun_range[1]})"
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="Provinsi"
)

st.plotly_chart(fig, use_container_width=True)

# =====================
# TABEL INTERAKTIF
# =====================
st.subheader("Tabel Data")

st.dataframe(
    df_filtered.sort_values(
        by=["Tahun", indikator],
        ascending=[True, False]
    ),
    use_container_width=True,
    height=450
)
