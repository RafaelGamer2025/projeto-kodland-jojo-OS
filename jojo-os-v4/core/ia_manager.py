
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# =========================
# 🔑 CLIENTE GROQ
# =========================
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =========================
# 🤖 IA PRINCIPAL
# =========================
def perguntar_ia(prompt):
    try:
        resposta = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Você é uma IA do sistema JOJO-OS."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return resposta.choices[0].message.content

    except Exception as e:
        return f"Erro IA: {e}"