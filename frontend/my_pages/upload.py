import sys
import os

# koneksi ke backend
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../backend")
    )
)

import streamlit as st
import google.generativeai as genai

from vision import analyze_food


# 🔥 helper biar aman dari error float
def safe_float(value):
    try:
        return float(value)
    except:
        return 0


def show():
    st.title("📸 Deteksi Makanan AI")

    st.caption("Upload gambar makanan untuk dianalisis oleh AI")

    image = st.file_uploader(
        "Upload gambar makanan",
        type=["jpg", "png", "jpeg"]
    )

    if image:
        st.image(image, caption="Gambar yang diupload")

        with st.spinner("🔍 Mendeteksi makanan..."):
            food_analysis = analyze_food(image)

        # reset pointer image (biar aman kalau dipakai lagi)
        image.seek(0)

        # 🔥 fallback biar ga error
        food_name = food_analysis.get("food", "Tidak diketahui")

        st.success(f"🍽️ Terdeteksi: {food_name}")

        # 🔥 safe parsing
        calories = safe_float(food_analysis.get("calories"))
        protein = safe_float(food_analysis.get("protein"))
        fat = safe_float(food_analysis.get("fat"))
        carbohydrate = safe_float(food_analysis.get("carbohydrate"))

        st.subheader("📊 Informasi Nutrisi")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🔥 Kalori", f"{calories} kkal")
            st.metric("🥩 Protein", f"{protein} g")

        with col2:
            st.metric("🥑 Lemak", f"{fat} g")
            st.metric("🍚 Karbohidrat", f"{carbohydrate} g")

        # 🔥 indikator visual
        st.progress(min(calories / 800, 1.0))

        st.subheader("🩺 Analisis Nutrisi")

        if calories < 200:
            st.success("Makanan ini termasuk rendah kalori dan cocok untuk camilan atau menu ringan.")
        elif calories < 500:
            st.info("Makanan ini memiliki jumlah kalori sedang dan cocok sebagai menu makan utama.")
        else:
            st.warning("Makanan ini tergolong tinggi kalori sehingga perlu diperhatikan porsinya.")

        st.subheader("💡 Analisis Mendalam dan Saran Konsumsi")

        try:
            model = genai.GenerativeModel("gemini-3.1-flash-lite")

            prompt = f"""
            Anda adalah ahli gizi.

            Nama makanan: {food_name}

            Berikan analisis:
            - manfaat
            - risiko jika berlebihan
            - saran konsumsi sehat

            Gunakan bahasa Indonesia sederhana.
            Jangan ulang angka nutrisi.
            """

            response = model.generate_content(prompt)

            st.write(response.text)

        except Exception as e:
            st.error(f"Gagal membuat analisis AI: {e}")


# 🔥 INI YANG BIKIN GA BLANK
if __name__ == "__main__":
    show()