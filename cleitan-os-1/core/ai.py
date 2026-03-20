from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=API_KEY)

def perguntar_ia(texto):
    resposta = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=texto
    )

    return resposta.text