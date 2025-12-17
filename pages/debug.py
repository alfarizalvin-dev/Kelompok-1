import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("DEBUG MAP – Indonesia")

# === LOAD DATA ===
df = pd.read_excel("Dataset.xlsx")

df["Provinsi"] = (
    df["Provinsi"]
    .str.strip()
    .str.title()
)

# pilih satu tahun
tahun = df["Tahun"].unique()[0]
df = df[df["Tahun"] == tahun]

# pastikan numerik
indikator = "IPM"  # GANTI jika perlu
df[indikator] = pd.to_numeric(df[indikator], errors="coerce")

# === LOAD GEOJSON ===
with open("indonesia_provinsi.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

st.write("Jumlah baris:", len(df))
st.write("Provinsi unik:", df["Provinsi"].nunique())

# === CHOROPLETH PALING MINIMAL ===
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="Provinsi",
    featureidkey="properties.PROVINSI",
    color=indikator,
)

fig.update_geos(
    fitbounds="geojson",
    visible=False
)

st.plotly_chart(fig, use_container_width=True)
