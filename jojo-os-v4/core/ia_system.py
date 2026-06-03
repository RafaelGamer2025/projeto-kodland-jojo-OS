import json
import os
import unicodedata
from difflib import get_close_matches
import random

DB_FILE = "data/users.json"

# =========================
# 🔧 NORMALIZA TEXTO
# =========================
def normalizar(texto):
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto


# =========================
# 💾 BANCO DE DADOS
# =========================
def carregar_db():
    try:
        pacote = carregar_db_seguro(DB_FILE)
        return pacote  # já retorna o db puro (sem "data")
    except:
        return {}
def salvar_db(db):
    salvar_db_seguro(db, DB_FILE)

# =========================
# 🧠 INTENÇÕES
# =========================
intencoes = {
    "saudacao": ["oi", "ola", "eae", "fala"],
    "nome": ["meu nome e", "sou", "eu sou"],
    "gosto": ["gosto de", "curto", "amo"],
    "idade": ["tenho", "idade"],
    "despedida": ["tchau", "adeus"],
    "batalha": ["lutar", "batalhar", "duelar"]
}


def detectar_intencao(texto):
    texto = normalizar(texto)

    todas = []
    mapa = {}

    for intent, frases in intencoes.items():
        for f in frases:
            todas.append(f)
            mapa[f] = intent

    match = get_close_matches(texto, todas, n=1, cutoff=0.6)

    if match:
        return mapa[match[0]]

    return "desconhecido"


# =========================
# 🆕 GARANTE USUÁRIO
# =========================
def garantir_user(db, user):
    if user not in db:
        db[user] = {
            "memoria": {},
            "stand": "Nenhum",
            "xp": 0,
            "level": 1
        }
    return db


# =========================
# 🌳 APRENDER SOBRE USUÁRIO
# =========================
def aprender_usuario(user, texto, db):
    texto = normalizar(texto)

    db = garantir_user(db, user)
    user_data = db[user]["memoria"]

    # Nome
    if "meu nome e" in texto:
        nome = texto.split("meu nome e")[-1].strip()
        user_data["nome"] = nome

    # Idade
    if "tenho" in texto:
        for p in texto.split():
            if p.isdigit():
                user_data["idade"] = p

    # Gostos
    if "gosto de" in texto:
        gosto = texto.split("gosto de")[-1].strip()
        user_data.setdefault("gostos", []).append(gosto)

    return db


# =========================
# ⚔️ SISTEMA DE STAND
# =========================
def escolher_stand(user, db, nome_stand):
    db = garantir_user(db, user)
    db[user]["stand"] = nome_stand
    salvar_db(db)
    return f"🔥 Stand {nome_stand} escolhido!"


def ganhar_xp(user, db, valor):
    db[user]["xp"] += valor

    if db[user]["xp"] >= 100:
        db[user]["level"] += 1
        db[user]["xp"] = 0
        return "✨ LEVEL UP!"

    return f"+{valor} XP"


# =========================
# ⚔️ BATALHA SIMPLES
# =========================
def batalha(user, db):
    db = garantir_user(db, user)

    stand = db[user]["stand"]

    if stand == "Nenhum":
        return "Você não tem Stand ainda!"

    dano = random.randint(10, 25)
    crit = random.random() < 0.2

    if crit:
        dano *= 2

    xp_msg = ganhar_xp(user, db, 20)

    salvar_db(db)

    return f"{stand} causou {dano} de dano! {'CRÍTICO!' if crit else ''}\n{xp_msg}"


# =========================
# 🤖 RESPOSTA
# =========================
def responder(user, texto):
    pacote = carregar_db()
    db = carregar_db()
    db = garantir_user(db, user)

    texto_norm = normalizar(texto)
    intent = detectar_intencao(texto_norm)

    db = aprender_usuario(user, texto, db)
    salvar_db(db)

    memoria = db[user]["memoria"]

    # =========================
    # RESPOSTAS
    # =========================

    if intent == "saudacao":
        return random.choice(["Olá humano.", "Eae.", "Fala aí."])

    if intent == "nome":
        return "Ok... vou lembrar disso."

    if intent == "gosto":
        return "Interessante..."

    if intent == "idade":
        return "Idade registrada."

    if intent == "despedida":
        return "Até mais..."

    if intent == "batalha":
        return batalha(user, db)

    # =========================
    # MEMÓRIA
    # =========================

    if "nome" in memoria:
        return f"{memoria['nome']}, explique melhor..."

    return "Não entendi..."


# =========================
# ❓ IA FAZ PERGUNTAS
# =========================
def perguntar_usuario(user):
    pacote = carregar_db()
    db = carregar_db()
    db = garantir_user(db, user)

    memoria = db[user]["memoria"]

    if "nome" not in memoria:
        return "Qual é seu nome?"

    if "idade" not in memoria:
        return "Quantos anos você tem?"

    if "gostos" not in memoria:
        return "O que você gosta?"

    if db[user]["stand"] == "Nenhum":
        return "Escolha um Stand: D4C, Tusk, The World..."

    return None