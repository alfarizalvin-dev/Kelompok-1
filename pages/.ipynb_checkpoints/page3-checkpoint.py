import streamlit as st
import pandas as pd
import os
import numpy as np
import altair as alt

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


# ======================================================
# 📊 PERBANDINGAN & TREN INDIKATOR ANTAR PROVINSI
# ======================================================

st.subheader("📊 Perbandingan & Tren Indikator Antar Provinsi")

# ===============================
# SATU FILTER INDIKATOR (GLOBAL)
# ===============================
indikator_pilihan = st.selectbox(
    "Pilih indikator",
    indikator
)

# Layout bersandingan
col1, col2 = st.columns(2)

# ======================================================
# 📊 PERBANDINGAN RATA-RATA ANTAR PROVINSI (BAR CHART)
# ======================================================
with col1:
    st.markdown("📊 **Perbandingan Rata-Rata Antar Provinsi**")

    if filtered_df.empty:
        st.warning("Data tidak tersedia untuk grafik perbandingan.")
    else:
        bar_df = (
            filtered_df
            .groupby(kol_prov)[indikator_pilihan]
            .mean()
            .reset_index()
            .sort_values(by=indikator_pilihan, ascending=False)
        )

        bar_chart = alt.Chart(bar_df).mark_bar().encode(
            x=alt.X(f"{indikator_pilihan}:Q", title="Nilai Rata-rata"),
            y=alt.Y(f"{kol_prov}:N", sort='-x', title="Provinsi"),
            tooltip=[kol_prov, indikator_pilihan]
        ).properties(
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)

# ======================================================
# 📈 TREN INDIKATOR ANTAR PROVINSI (LINE CHART)
# ======================================================
with col2:
    st.markdown("📈 **Tren Indikator Antar Provinsi**")

    if filtered_df.empty:
        st.warning("Data tidak tersedia untuk grafik tren.")
    else:
        tren_df = (
            filtered_df
            .groupby([kol_tahun, kol_prov])[indikator_pilihan]
            .mean()
            .reset_index()
        )

        if tren_df.empty:
            st.warning("Data tidak cukup untuk menampilkan tren.")
        else:
            line_chart = alt.Chart(tren_df).mark_line(point=True).encode(
                x=alt.X(f"{kol_tahun}:O", title="Tahun"),
                y=alt.Y(f"{indikator_pilihan}:Q", title="Nilai"),
                color=alt.Color(f"{kol_prov}:N", title="Provinsi"),
                tooltip=[kol_prov, kol_tahun, indikator_pilihan]
            ).properties(
                height=400
            )

            st.altair_chart(line_chart, use_container_width=True)

st.markdown("### ⬇️ Unduh Data yang Ditampilkan")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download data (CSV)",
    data=csv,
    file_name="data_terfilter_page3.csv",
    mime="text/csv"
)


# ===============================
# VALIDASI DATA SEBELUM ANALISIS
# ===============================
if filtered_df.empty or len(provinsi) == 0:
    st.info("👆 Pilih minimal satu wilayah untuk menampilkan analisis dan kesimpulan.")
    st.stop()


# ===============================
# ANALISIS DATA (PARAGRAF + HIGHLIGHT OTOMATIS)
# ===============================
st.subheader("🔍 Analisis Data")

paragraf = []

for col in indikator:
    tren = filtered_df.groupby(kol_tahun)[col].mean()

    # Tentukan arah tren
    if len(tren) < 2:
        arah = "stabil"
        warna = "#facc15"  # kuning
        ikon = "🟡"
    elif tren.iloc[-1] > tren.iloc[0]:
        arah = "mengalami peningkatan"
        warna = "#16a34a"  # hijau
        ikon = "🟢"
    else:
        arah = "mengalami penurunan"
        warna = "#dc2626"  # merah
        ikon = "🔴"

    nilai_rata = mean_values[col]

    # Kalimat utama + highlight warna
    kalimat = f"""
    <span style="
        background-color:{warna}22;
        padding:6px 10px;
        border-radius:8px;
        display:inline-block;
        margin-bottom:6px;
    ">
    {ikon} <b>{col.replace('_',' ').upper()}</b> memiliki rata-rata sebesar
    <b>{nilai_rata:.2f}</b> dan secara umum <b>{arah}</b> selama periode pengamatan.
    </span>
    """

    # Interpretasi kontekstual
    if "ahh" in col:
        kalimat += " Peningkatan ini mencerminkan perbaikan kualitas kesehatan dan layanan publik."
    elif "aml" in col or "rls" in col:
        kalimat += " Hal ini menunjukkan kemajuan akses dan kualitas pendidikan."
    elif "ppm" in col or "miskin" in col:
        kalimat += " Perubahan ini mengindikasikan dinamika tingkat kesejahteraan masyarakat."
    elif "tpt" in col:
        kalimat += " Kondisi ini mencerminkan situasi pasar tenaga kerja di wilayah tersebut."
    elif "ipm" in col:
        kalimat += " IPM yang meningkat menunjukkan kemajuan pembangunan manusia secara komprehensif."
    elif "gini" in col:
        kalimat += " Penurunan ketimpangan berkontribusi pada pertumbuhan yang lebih inklusif."
    elif "inflasi" in col:
        kalimat += " Stabilitas inflasi penting untuk menjaga daya beli masyarakat."
    elif "pdrb" in col:
        kalimat += " Peningkatan PDRB per kapita mencerminkan membaiknya kapasitas ekonomi daerah."
    elif "growth" in col or "pertumbuhan" in col:
        kalimat += " Perlambatan pertumbuhan perlu menjadi perhatian dalam perumusan kebijakan."

    paragraf.append(f"<p style='margin-bottom:14px; text-align:justify'>{kalimat}</p>")

# Gabungkan semua paragraf
analisis_html = "".join(paragraf)

# Tampilkan dalam container rapi
st.markdown(
    f"""
    <div style="
        background-color:#f8fafc;
        padding:22px;
        border-radius:14px;
        border-left:6px solid #2563eb;
    ">
    {analisis_html}
    </div>
    """,
    unsafe_allow_html=True
)




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
