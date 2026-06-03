import hashlib
import json
import os
from dotenv import load_dotenv
import requests

# 🔐 verificador de maquinas
def verificar_maquina():
    try:
        # Consulta o IP público e localização
        response = requests.get('https://ipapi.co')
        data = response.json()

        print("--- Detalhes da Máquina ---")
        print(f"IP Público: {data.get('ip')}")
        print(f"País: {data.get('country_name')} ({data.get('country')})")
        print(f"Região: {data.get('region')}")
        print(f"Cidade: {data.get('city')}")
        print(f"Provedor: {data.get('org')}")

        # Verificação específica Bulgária
        if data.get('country') == 'BG':
            print("\nResultado: Máquina na BULGÁRIA detectada.")
        else:
            print("\nResultado: Máquina fora da Bulgária.")

    except Exception as e:
        print(f"Erro ao obter dados: {e}")

if __name__ == "__main__":
    verificar_maquina()

load_dotenv()

# 🔐 HASH DE SENHA
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# 🔐 GERAR ASSINATURA DO BANCO
def gerar_assinatura(data, key):
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256((raw + key).encode()).hexdigest()

# 🔐 PEGAR CHAVE DO SISTEMA (ARQUIVO LOCAL)
def get_system_key():
    if not os.path.exists("data/system_key.json"):
        raise Exception("❌ system_key.json não encontrado!")

    with open("data/system_key.json") as f:
        return json.load(f)["key"]

# 🔐 SALVAR BANCO COM ASSINATURA
def salvar_db_seguro(db, caminho):
    key = get_system_key()
    assinatura = gerar_assinatura(db, key)

    pacote = {
        "data": db,
        "assinatura": assinatura
    }

    with open(caminho, "w") as f:
        json.dump(pacote, f, indent=4)

# 🔐 CARREGAR BANCO COM PROTEÇÃO
def carregar_db_seguro(caminho):
    if not os.path.exists(caminho):
        return {}

    with open(caminho) as f:
        pacote = json.load(f)

    db = pacote.get("data", {})
    assinatura_salva = pacote.get("assinatura")

    key = get_system_key()
    assinatura_real = gerar_assinatura(db, key)

    # 🚨 DETECTOU HACK
    if assinatura_real != assinatura_salva:
        return {"__hack_detected__": True, "data": db}
        print("🚨 HACK DETECTADO! BANCO CORROMPIDO OU ALTERADO! 🚨")
        if admin := input("Você é o administrador? (s/n) ").lower() == "s":
            if input("Digite a chave do sistema para recuperar: ") == key:
                print("✅ Chave correta! Recuperando banco...")
                print("🔑 Chave do sistema:", key)
                
                return db
            else:
                print("❌ Chave incorreta! Acesso negado.")
                return {"__hack_detected__": True, "data": db}

    return db