import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Analisis Indikator Pembangunan Provinsi")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    return pd.read_excel("Dataset.xlsx")

df = load_data()

# Rapikan data
df["Provinsi"] = df["Provinsi"].str.strip().str.title()
df["Tahun"] = df["Tahun"].astype(int)

# =====================
# DAFTAR INDIKATOR
# =====================
indikator_list = [
    "AHH",
    "AML",
    "PPM",
    "RLS",
    "TPT",
    "IPM",
    "E_Growth",
    "Laju_Pertumbuhan",
    "PDRB_Kapita",
    "Inflasi_(YoY)",
    "Gini_Ratio"
]
# =====================
# DEFINISI INDIKATOR
# =====================
indikator_nama = {
    "AHH": "Angka Harapan Hidup",
    "AML": "Angka Melek Huruf",
    "PPM": "Penduduk Miskin",
    "RLS": "Rata-rata Lama Sekolah",
    "TPT": "Tingkat Pengangguran Terbuka",
    "IPM": "Indeks Pembangunan Manusia",
    "E_Growth": "Pertumbuhan Ekonomi",
    "Laju_Pertumbuhan": "Laju Pertumbuhan",
    "PDRB_Kapita": "PDRB per Kapita",
    "Inflasi_(YoY)": "Inflasi (Year-on-Year)",
    "Gini_Ratio": "Gini Ratio"
}

indikator_definisi = {
    "AHH": "Angka Harapan Hidup (AHH) adalah rata-rata perkiraan jumlah tahun hidup yang akan dijalani seseorang sejak lahir, yang mencerminkan derajat kesehatan masyarakat.",
    "AML": "Angka Melek Huruf (AML) adalah persentase penduduk usia 15 tahun ke atas yang mampu membaca dan menulis sebagai indikator dasar kualitas pendidikan.",
    "PPM": "Penduduk Miskin (PPM) menunjukkan persentase penduduk yang berada di bawah garis kemiskinan.",
    "RLS": "Rata-rata Lama Sekolah (RLS) adalah rata-rata jumlah tahun pendidikan formal yang telah ditempuh oleh penduduk usia 25 tahun ke atas.",
    "TPT": "Tingkat Pengangguran Terbuka (TPT) adalah persentase angkatan kerja yang belum bekerja dan sedang mencari pekerjaan.",
    "IPM": "Indeks Pembangunan Manusia (IPM) merupakan indeks komposit yang mengukur capaian pembangunan manusia dari sisi kesehatan, pendidikan, dan standar hidup.",
    "E_Growth": "Economic Growth (Pertumbuhan Ekonomi) adalah persentase perubahan Produk Domestik Regional Bruto (PDRB) riil dari satu periode ke periode berikutnya.",
    "Laju_Pertumbuhan": "Laju Pertumbuhan menggambarkan kecepatan pertumbuhan ekonomi suatu wilayah dalam periode tertentu.",
    "PDRB_Kapita": "PDRB per Kapita adalah nilai PDRB dibagi jumlah penduduk, mencerminkan rata-rata pendapatan per orang.",
    "Inflasi_(YoY)": "Inflasi Year-on-Year (YoY) menunjukkan persentase kenaikan harga umum dibandingkan periode yang sama tahun sebelumnya.",
    "Gini_Ratio": "Gini Ratio mengukur tingkat ketimpangan distribusi pendapatan dalam suatu wilayah."
}

# =====================
# DEFINISI INDIKATOR
# =====================
indikator_definisi = {
    "AHH": "Angka Harapan Hidup (AHH) adalah rata-rata perkiraan jumlah tahun hidup yang akan dijalani seseorang sejak lahir, yang mencerminkan derajat kesehatan masyarakat.",
    "AML": "Angka Melek Huruf (AML) adalah persentase penduduk usia 15 tahun ke atas yang mampu membaca dan menulis, sebagai indikator dasar kualitas pendidikan.",
    "PPM": "Pengeluaran Per Kapita (PPM) merupakan rata-rata pengeluaran konsumsi penduduk per orang dalam periode tertentu, yang mencerminkan tingkat kesejahteraan ekonomi.",
    "RLS": "Rata-rata Lama Sekolah (RLS) adalah rata-rata jumlah tahun pendidikan formal yang telah ditempuh oleh penduduk usia 25 tahun ke atas.",
    "TPT": "Tingkat Pengangguran Terbuka (TPT) adalah persentase angkatan kerja yang tidak bekerja dan sedang mencari pekerjaan terhadap total angkatan kerja.",
    "IPM": "Indeks Pembangunan Manusia (IPM) merupakan indeks komposit yang mengukur capaian pembangunan manusia melalui dimensi kesehatan, pendidikan, dan standar hidup layak.",
    "E_Growth": "Economic Growth (Pertumbuhan Ekonomi) adalah persentase perubahan Produk Domestik Regional Bruto (PDRB) riil dari satu periode ke periode berikutnya.",
    "Laju_Pertumbuhan": "Laju Pertumbuhan menunjukkan persentase perubahan suatu variabel ekonomi dalam periode tertentu.",
    "PDRB_Kapita": "PDRB per Kapita adalah nilai Produk Domestik Regional Bruto dibagi jumlah penduduk.",
    "Inflasi_(YoY)": "Inflasi Year-on-Year (YoY) adalah persentase kenaikan harga barang dan jasa dibandingkan periode yang sama pada tahun sebelumnya.",
    "Gini_Ratio": "Gini Ratio adalah ukuran ketimpangan distribusi pendapatan dengan nilai antara 0 hingga 1."
}

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
# DEFINISI INDIKATOR (DINAMIS)
# =====================
st.subheader(f"📘 Definisi {indikator} ({indikator_nama[indikator]})")
st.info(indikator_definisi[indikator])

# =====================
# FILTER DATA
# =====================
df_filtered = df[
    (df["Provinsi"].isin(provinsi)) &
    (df["Tahun"].between(tahun_range[0], tahun_range[1]))
].copy()

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
