import streamlit as st
import requests

# =========================
# 🧠 REKOMENDASI ENGINE
# =========================
def get_rekomendasi(risiko, bmi):
    rec = []

    if risiko == 0:
        rec.append("Pertahankan aktivitas fisik secara rutin")
        rec.append("Pertahankan pola tidur 7–8 jam per hari")
        rec.append("Jaga pola makan seimbang")
        rec.append("Perbanyak konsumsi sayur dan buah")
    else:
        rec.append("Kurangi makanan cepat saji")
        rec.append("Rutin olahraga minimal 3–4 kali seminggu")
        rec.append("Perbaiki pola tidur")
        rec.append("Kurangi makanan tinggi lemak dan gula")

    # tambahan berdasarkan BMI
    if bmi >= 25:
        rec.append("Turunkan berat badan secara bertahap")

    return rec


# =========================
# 🚀 MAIN PAGE
# =========================
def show():
    st.header("⚠️ Prediksi Risiko Kesehatan")

    # ================= INPUT USER =================
    nama = st.text_input("Nama Lengkap", "Masukkan Nama Anda")

    umur = st.number_input("Umur", 0, 120, 23)

    gender = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])

    tinggi = st.number_input("Tinggi Badan (cm)", 100, 220, 160)

    berat = st.number_input("Berat Badan (kg)", 30, 200, 55)

    aktivitas = st.selectbox("Aktivitas Fisik", [
        "Jarang",
        "1–2 Kali/Minggu",
        "3–4 Kali/Minggu",
        "Hampir Setiap Hari"
    ])

    tidur = st.number_input("Durasi Tidur (Jam/Hari)", 0, 24, 7)

    riwayat = st.selectbox("Riwayat Diabetes Keluarga", ["Tidak", "Ada"])

    fast_food = st.selectbox("Konsumsi Makanan Cepat Saji", [
        "Tidak Pernah",
        "1–2 Kali/Minggu",
        "3–4 Kali/Minggu",
        "Setiap Hari"
    ])

    # ================= PREDIKSI =================
    if st.button("Prediksi"):

        with st.spinner("🔍 Menganalisis kesehatan..."):
            res = requests.post(
                "http://127.0.0.1:8000/predict/",
                json={"umur": umur, "bmi": 0}
            )

        hasil = res.json()

        if "error" in hasil:
            st.error(hasil["error"])
            return

        # ================= HITUNG BMI =================
        bmi = berat / ((tinggi / 100) ** 2)

        if bmi < 18.5:
            kategori = "Kurus"
        elif bmi < 25:
            kategori = "Normal"
        elif bmi < 30:
            kategori = "Overweight"
        else:
            kategori = "Obesitas"

        risiko_text = "Rendah" if hasil["risiko"] == 0 else "Tinggi"

        rekomendasi = get_rekomendasi(hasil["risiko"], bmi)

        # ================= OUTPUT =================
        st.subheader("📊 Hasil Analisis Kesehatan")

        st.markdown(f"""
**Nama Lengkap**    : {nama}  
**Umur**            : {umur} Tahun  
**Jenis Kelamin**   : {gender}  
**Tinggi Badan**    : {tinggi} cm  
**Berat Badan**     : {berat} kg  
**Aktivitas Fisik** : {aktivitas}  
**Durasi Tidur**    : {tidur} Jam/Hari  
**Riwayat Diabetes Keluarga** : {riwayat}  
**Konsumsi Fast Food** : {fast_food}  

---

### 🧮 BMI : {bmi:.1f} ({kategori})

### ⚠️ Prediksi Risiko Kesehatan : {risiko_text}
""")

        # ================= REKOMENDASI (FIXED) =================
        st.markdown("### 💡 Rekomendasi")

        for r in rekomendasi:
            st.success("✓ " + r)