import sys
import os
import streamlit as st

sys.path.append(os.path.abspath("frontend"))

from my_pages import dashboard, nutrisi, prediksi, upload, chat

st.set_page_config(layout="wide")
st.markdown("""
<style>

/* 🔥 HEADER CONTAINER */
.header {
    position: sticky;
    top: 0;
    z-index: 999;
    color: white;
    padding: 10px 20px;
    border-bottom: 1px solid #ddd;
    background: linear-gradient(180deg, #00c853, #2e7d32);
}

/* 🔥 FLEX */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* 🔥 KIRI */
.header-left {
    font-size: 20px;
    font-weight: bold;
}

/* 🔥 KANAN */
.header-right {
    display: flex;
    gap: 15px;
    align-items: center;
}

/* 🔥 ICON STYLE */
.header-icon {
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 8px;
}

.header-icon:hover {
    background-color: #f0f0f0;
}

</style>

<div class="header">
    <div class="header-container">
        <div class="header-left">🍃 NutriGen.AI</div>
        <div class="header-right">
            <div class="header-icon">🔔</div>
            <div class="header-icon">👤 Admin</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# hide bawaan streamlit
st.markdown("""
<style>

/* ❌ Hapus header default Streamlit */
header[data-testid="stHeader"] {
    display: block;
}

/* ❌ Hapus menu kanan atas (Deploy, dll) */
#MainMenu {
    visibility: hidden;
}

/* ❌ Optional: footer */
footer {
    visibility: hidden;
}

/* 🔥 Hilangin padding atas biar mepet */
.block-container {
    padding-top: 1rem !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* 🔥 Background sidebar gradient */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #00c853, #2e7d32);
    color: white;
}

/* 🔥 Text sidebar jadi putih */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* 🔥 Radio button (menu) */
div[role="radiogroup"] > label {
    background-color: transparent !important;
    padding: 10px;
    border-radius: 8px;
}

/* 🔥 Hover menu */
div[role="radiogroup"] > label:hover {
    background-color: rgba(255,255,255,0.2) !important;
}

/* 🔥 Menu aktif (dipilih) */
div[role="radiogroup"] > label[data-selected="true"] {
    background-color: rgba(0,0,0,0.3) !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ✅ SIDEBAR LANGSUNG DI SINI
st.sidebar.title("🥗 NutriGen.AI")
st.sidebar.caption("AI Nutrisi & Kesehatan")

menu = st.sidebar.radio(
    "Menu",
    ["Analisis Nutrisi", "Prediksi Kesehatan", "Chatbot AI", "Deteksi Makanan", "Dashboard"]
)

# st.title("🥗 NutriGen.AI")


# ✅ ROUTING PAGE
if menu == "Dashboard":
    dashboard.show()

if menu == "Analisis Nutrisi":
    nutrisi.show()

elif menu == "Prediksi Kesehatan":
    prediksi.show()

elif menu == "Chatbot AI":
    chat.show()

elif menu == "Deteksi Makanan":
    upload.show()