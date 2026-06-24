import streamlit as st

st.markdown("""
<style>

/* SIDEBAR UTAMA */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #16a34a, #22c55e, #4ade80) !important;
}

/* SEMUA CONTAINER DALAM SIDEBAR */
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* SEMUA ELEMEN DALAM SIDEBAR */
section[data-testid="stSidebar"] * {
    color: white !important;
    background-color: transparent !important;
}

/* KHUSUS BUTTON */
section[data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 10px;
    border: none;
    width: 100%;
}

/* HOVER BUTTON */
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255,255,255,0.3) !important;
}

/* HILANGKAN BORDER */
section[data-testid="stSidebar"] {
    border-right: none !important;
}

</style>
""", unsafe_allow_html=True)
def render_sidebar():
    st.sidebar.title("🥗 NutriGen.AI")
    st.sidebar.caption("AI Nutrisi & Kesehatan")

    # default menu
    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"

    # 🔥 tombol menu
    if st.sidebar.button("📊 Dashboard"):
        st.session_state.menu = "Dashboard"

    if st.sidebar.button("🍱 Analisis Nutrisi"):
        st.session_state.menu = "Analisis Nutrisi"

    if st.sidebar.button("⚠️ Prediksi Kesehatan"):
        st.session_state.menu = "Prediksi Kesehatan"

    return st.session_state.menu