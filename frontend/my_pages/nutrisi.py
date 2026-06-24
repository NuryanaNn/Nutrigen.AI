import streamlit as st
import requests

# ==============================
# 🎨 STYLE GAMBAR + CARD
# ==============================
st.markdown("""
<style>

/* gambar rapi */
img {
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
    border-radius: 10px;
}

/* card makanan */
.food-card {
    background: #ffffff;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* teks kecil & rapi */
.food-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
}

.food-info {
    font-size: 13px;
    line-height: 1.6;
    color: #333;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# 🖼️ DEFAULT IMAGE
# ==============================
DEFAULT_IMG = "https://via.placeholder.com/300x200?text=No+Image"


# ==============================
# 🔍 VALIDASI IMAGE
# ==============================
@st.cache_data
def is_valid_image(url):
    try:
        res = requests.head(url, timeout=3)
        return res.status_code == 200
    except:
        return False


# ==============================
# 🖼️ SHOW IMAGE
# ==============================
def show_image(url):
    if url and is_valid_image(url):
        st.image(url)
    else:
        st.image(DEFAULT_IMG)
        st.caption("⚠️ Gambar tidak tersedia")


# ==============================
# 🚀 MAIN PAGE
# ==============================
def show():
    st.header("🍱 Cek Nutrisi Makanan")

    # INIT SESSION STATE
    if "history_makanan" not in st.session_state:
        st.session_state.history_makanan = []

    if "total_cek" not in st.session_state:
        st.session_state.total_cek = 0

    if "total_protein" not in st.session_state:
        st.session_state.total_protein = 0

    # INPUT
    food = st.text_input("Masukkan nama makanan")

    filter_option = st.selectbox(
        "Filter",
        ["Semua", "Rendah Kalori", "Tinggi Protein"]
    )

    # FETCH DATA
    if st.button("Cek Nutrisi"):
        if not food:
            st.warning("⚠️ Masukkan nama makanan dulu")
            return

        with st.spinner("🔍 Mencari makanan..."):
            try:
                res = requests.get(f"http://127.0.0.1:8000/nutrition/{food}")
                data = res.json()
            except:
                st.error("❌ Gagal koneksi ke server")
                return

        # ERROR HANDLING
        if isinstance(data, dict) and "error" in data:
            st.warning(data["error"])
            return

        if not data:
            st.info("Data tidak ditemukan")
            return

        # SAVE HISTORY
        st.session_state.history_makanan.extend(data)
        st.session_state.total_cek += len(data)

        avg_protein = sum(d.get("proteins", 0) for d in data) / len(data)
        st.session_state.total_protein = round(avg_protein, 2)

        # FILTER
        filtered_data = data

        if filter_option == "Rendah Kalori":
            filtered_data = [d for d in data if d.get("calories", 0) < 200]

        elif filter_option == "Tinggi Protein":
            filtered_data = [d for d in data if d.get("proteins", 0) > 10]

        # ==============================
        # 🧱 TAMPILAN CARD UI (NEW)
        # ==============================
        cols = st.columns(3)

        for i, item in enumerate(filtered_data):
            with cols[i % 3]:

                st.markdown('<div class="food-card">', unsafe_allow_html=True)

                # TITLE
                st.markdown(
                    f"<div class='food-title'>{item.get('name', '-')}</div>",
                    unsafe_allow_html=True
                )

                # IMAGE
                show_image(item.get("image"))

                # INFO (CUSTOM TEXT, LEBIH KECIL)
                st.markdown(f"""
                <div class="food-info">
                    🍗 Kalori: <b>{item.get('calories', 0)} kcal</b><br>
                    💪 Protein: <b>{item.get('proteins', 0)} g</b><br>
                    🥑 Lemak: <b>{item.get('fat', 0)} g</b><br>
                    🍞 Karbo: <b>{item.get('carbohydrate', 0)} g</b>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                st.divider()