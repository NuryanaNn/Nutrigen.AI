import streamlit as st
import pandas as pd
import os

# 🔥 WAJIB (biar full width)
st.set_page_config(layout="wide")

def load_data():
    base_dir = os.path.dirname(os.getcwd())
    path = os.path.join(base_dir, "backend", "data", "nutrition.csv")

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def show():
    st.header("📊 Dashboard NutriGen.AI")

    df = load_data()

    # ==============================
    # 🎯 HITUNG DATA
    # ==============================
    total_cek = len(df)

    total_protein = 0
    total_risiko = 0

    if not df.empty:
        total_protein = round(df["proteins"].mean(), 2)
        total_risiko = len(df[df["calories"] > 300])

    # ==============================
    # 🎨 STYLE
    # ==============================
    st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-family: sans-serif;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .blue { background: linear-gradient(135deg, #36A2EB, #007bff); }
    .red { background: linear-gradient(135deg, #ff4b5c, #c0392b); }
    .green { background: linear-gradient(135deg, #2ecc71, #27ae60); }

    .title { font-size: 18px; margin-bottom: 10px; }
    .value { font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # ==============================
    # 🎯 CARD (3 KOLOM)
    # ==============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card blue">
            <div class="title">🍱 Total Cek</div>
            <div class="value">{total_cek}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card red">
            <div class="title">⚠️ Risiko</div>
            <div class="value">{total_risiko}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card green">
            <div class="title">💪 Protein</div>
            <div class="value">{total_protein} g</div>
        </div>
        """, unsafe_allow_html=True)

    # ==============================
    # 🔥 CHART (FULL WIDTH)
    # ==============================
    st.markdown("---")
    st.subheader("📈 Statistik Nutrisi")
    if df.empty:
        st.info("Belum ada data")
        return

    # 📈 Trend Protein
    st.markdown("### 💪 Trend Protein")
    st.line_chart(df["proteins"], use_container_width=True)

    # 📊 Kalori per makanan
    st.markdown("### 🍗 Kalori per Makanan")
    st.bar_chart(df.set_index("name")["calories"], use_container_width=True)

    # ⚠️ Distribusi Risiko
    st.markdown("### ⚠️ Distribusi Risiko")

    aman = len(df[df["calories"] <= 300])
    risiko = len(df[df["calories"] > 300])

    chart_data = pd.DataFrame({
        "Kategori": ["Aman", "Risiko"],
        "Jumlah": [aman, risiko]
    })

    st.bar_chart(chart_data.set_index("Kategori"), use_container_width=True)