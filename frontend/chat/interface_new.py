import uuid
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from chat.qdrant_manage_new import save_chat, retrieve_chat_memory, retrieve_knowledge
from langchain.agents import create_agent
from chat.tools import target_weight, calculate_bmi

load_dotenv()

# init LLM (sekali saja)
client = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API"),
    temperature=0
)

# 🔥 FUNCTION UTAMA
def chat_ai(user_input, session_id=None):

    if session_id is None:
        session_id = str(uuid.uuid4())

    # =========================
    # 🔎 BUILD HISTORY
    # =========================
    def build_history_context(session_id):
        history = retrieve_chat_memory(session_id)

        if len(history) == 0:
            return ""

        history_text = ""
        for point in history:
            role = point.payload["role"]
            content = point.payload["content"]

            history_text += f"{role}: {content}\n"

        return history_text

    history_context = build_history_context(session_id)

    # =========================
    # 🧠 SYSTEM PROMPT
    # =========================
    system_prompt = """
Anda adalah NutriGen AI.

TOOLS:

1. retrieve_knowledge
Gunakan untuk mencari informasi nutrisi dan kesehatan.

2. calculate_bmi
Gunakan ketika pengguna menyebutkan tinggi dan berat badan.

3. target_weight
Gunakan untuk menghitung berat badan ideal.

ATURAN:

- Gunakan retrieve_knowledge untuk menjawab fakta kesehatan dan nutrisi.
- Gunakan calculate_bmi ketika tersedia tinggi dan berat badan.
- Gunakan target_weight untuk rekomendasi berat badan ideal.
- Jika pertanyaan di luar domain kesehatan dan nutrisi maka jawab:

Maaf, saya hanya bisa membantu dengan topik yang relevan dengan kesehatan dan nutrisi.
"""

    # =========================
    # 🤖 AGENT
    # =========================
    agent = create_agent(
        model=client,
        tools=[
            retrieve_knowledge,
            calculate_bmi,
            target_weight
        ],
        system_prompt=system_prompt
    )

    response = agent.invoke({
        "messages": [
            {
                "role": "system",
                "content": f"Riwayat percakapan:\n{history_context}"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    answer = response["messages"][-1].content

    # =========================
    # 💾 SAVE MEMORY
    # =========================
    save_chat(session_id, "user", user_input)
    save_chat(session_id, "assistant", answer)

    return answer, session_id