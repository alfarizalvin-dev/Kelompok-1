import streamlit as st

pages = [
    st.Page(page="pages/page1.py", title="Literacy", icon="🏠"),
    st.Page(page="pages/page2.py", title="Global Literacy", icon="📊"),
    st.Page(page="pages/page3.py", title="Analisis Data & Kesimpulan", icon="⚙️")
]

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

pg.run()
