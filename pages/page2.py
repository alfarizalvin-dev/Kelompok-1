import streamlit as st
import pandas as pd
import plotly.express as px
import json

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Dashboard Indikator Provinsi Indonesia",
    layout="wide"
)

st.title("📊 Dashboard Indikator Provinsi Indonesia")
st.markdown("---")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset.xlsx")
    return df

@st.cache_data
def load_geojson():
    with open("indonesia_provinsi.geojson", "r", encoding="utf-8") as f:
        geo = json.load(f)
    return geo

df = load_data()
geojson = load_geojson()

# -----------------------
# SIDEBAR FILTER
# -----------------------
st.sidebar.header("🔎 Filter Data")

tahun = st.sidebar.selectbox(
    "Pilih Tahun",
    sorted(df["Tahun"].unique())
)

indikator = st.sidebar.selectbox(
    "Pilih Indikator",
    ["AHH", "AML", "PPM", "RLS", "TPT", "IPM", "E_Growth", "Laju Pertumbuhan", "PDRB_Kapita", "Gini_Ratio"]
)

# Filter data
df_filtered = df[df["Tahun"] == tahun]

# -----------------------
# CHOROPLETH MAP
# -----------------------
st.subheader("🗺️ Peta Indikator Provinsi Indonesia")

fig_map = px.choropleth(
    df_filtered,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.name",
    color=indikator,
    color_continuous_scale="Viridis",
    hover_name="Provinsi",
    hover_data={indikator: True},
    title=f"Peta {indikator} Provinsi Indonesia Tahun {tahun}"
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map.update_layout(
    height=600,
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------
# INTERACTIVE TABLE
# -----------------------
st.subheader("📋 Tabel Data Provinsi")

# Sorting
sort_col = st.selectbox(
    "Urutkan Berdasarkan",
    ["Provinsi", indikator]
)

sort_order = st.radio(
    "Urutan",
    ["Terbesar ke Terkecil", "Terkecil ke Terbesar"],
    horizontal=True
)

ascending = sort_order == "Terkecil ke Terbesar"

df_table = df_filtered.sort_values(
    by=sort_col,
    ascending=ascending
)

st.dataframe(
    df_table,
    use_container_width=True,
    height=500
)
