from core.security import salvar_db_seguro
import json

caminho = "data/users.json"

# carrega como normal (sem validação)
with open(caminho) as f:
    pacote = json.load(f)

db = pacote.get("data", {})

# salva novamente com assinatura nova
salvar_db_seguro(db, caminho)

print("✅ Banco re-assinado com sucesso!")