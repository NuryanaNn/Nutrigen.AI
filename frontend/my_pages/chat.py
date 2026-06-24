import sys
import os

# koneksi ke AI engine
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../chat")
    )
)

import streamlit as st
from chat.interface_new import chat_ai

# 🔥 INI YANG KURANG
def show():
    st.header("💬 NutriGen AI Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    # tampilkan history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Tanya tentang nutrisi...")

    if user_input:

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        answer, session_id = chat_ai(
            user_input,
            st.session_state.session_id
        )

        st.session_state.session_id = session_id

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)