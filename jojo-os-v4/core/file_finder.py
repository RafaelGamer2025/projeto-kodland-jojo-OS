import os

# cache para não ficar lento
_cache = {}

def buscar_arquivo(nome_arquivo):
    """
    Procura arquivo dentro do projeto JOJO-OS (não global)
    """
    if nome_arquivo in _cache:
        return _cache[nome_arquivo]

    # pega raiz do projeto (1 nível acima de /core)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    for root, dirs, files in os.walk(project_root):
        if nome_arquivo in files:
            caminho = os.path.join(root, nome_arquivo)
            _cache[nome_arquivo] = caminho
            return caminho

    return None