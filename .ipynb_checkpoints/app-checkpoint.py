import streamlit as st

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Kelompok 1 Prak Big Data",
    layout="wide"
)

# =========================
# KONTEN HALAMAN UTAMA
# =========================
st.title("Beranda")
st.write("Gunakan sidebar di sebelah kiri untuk berpindah halaman.")

# =========================
# STYLE (AMAN & TIDAK MERUSAK NAVIGASI)
# =========================
st.markdown(
    """
    <style>
    /* MAIN CONTENT */
    section[data-testid="stMain"] {
        background-color: #EBF4DD;
        padding: 2rem;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #5A7863;
    }

    /* FONT SIDEBAR */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* JUDUL */
    h1, h2, h3 {
        color: #2F4F3F;
    }
    </style>
    """,
    unsafe_allow_html=True
)
