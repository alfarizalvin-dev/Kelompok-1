import streamlit as st

pages = [
    st.Page(page="pages/page1.py", title="Home", icon="🏠"),
    st.Page(page="pages/page2.py", title="Visualisasi Data", icon="📊"),
    st.Page(page="pages/page3.py", title="Analisis Data & Kesimpulan", icon="⚙️")
]

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()

st.markdown(
    """
    <style>
    /* =========================
       KONTEN TENGAH (MAIN AREA)
       ========================= */
    section[data-testid="stMain"] {
        background-color: #EBF4DD; /* hijau muda solid */
        padding: 2rem;
    }

    /* =========================
       SIDEBAR
       ========================= */
    section[data-testid="stSidebar"] {
        background-color: #5A7863; /* hijau tua */
    }

    /* =========================
       FONT SIDEBAR
       ========================= */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* font putih */
    }

    /* Label selectbox & slider */
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* Dropdown & input tetap readable */
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* =========================
       JUDUL KONTEN
       ========================= */
    h1, h2, h3 {
        color: #2F4F3F; /* hijau gelap elegan */
    }
    </style>
    """,
    unsafe_allow_html=True
)



