# Cleitan-OS 🚀

O **Cleitan-OS** é uma ferramenta multifuncional desenvolvida em Python para análise de sistemas, segurança e automação. O projeto utiliza Inteligência Artificial (Google Gemini) para processamento de dados e oferece módulos especializados para varredura de rede e utilitários de sistema, além de jogos e animações.

---

## 🛠️ Funcionalidades

* **Módulo de IA (`core/ai.py`):** Integração com o Google Generative AI para análises inteligentes.
* **Scanner de Portas (`core/ports.py`):** Ferramenta para verificação de portas abertas e serviços.
* **Scanner de Rede/Web (`core/scanner.py`):** Varredura estruturada para busca de informações e padrões.
* **Calculadora (`core/calc_window.py`):** Uma calculadora com interface gráfica para operações matemáticas.
* **Interface Intuitiva (`ui/interface.py`):** Interface de linha de comando (CLI) organizada para facilitar o uso.
* **Menu Flutuante (`ui/mod_menu.py`):** Acesso rápido a diferentes aplicativos do Cleitan-OS.
* **Animação de Matrix (`ui/matrix_animation.py`):** Efeito visual de letras descendo, semelhante ao filme Matrix.
* **Navegador Estilo Hacker (`ui/browser.py`):** Acesso ao Chrome ou um navegador personalizado.
* **Jogo em Pygame (`games/pygame_game/main.py`):** Um jogo interativo utilizando imagens e sons.

---

## 🚀 Como instalar

### Pré-requisitos
* **Python 3.10** ou superior.
* Uma chave de API do **Google Gemini** (Obtenha no [AI Studio](https://aistudio.google.com/)).

### Passo a passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/RafaelGamer2025/projeto-kodland-cleitan-os
   cd projeto-kodland-cleitan-os
   ```
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure suas variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto e adicione sua chave da API do Google Gemini:
   ```
   GEMINI_KEY=your_api_key_here
   ```

---

## 🎮 Como jogar

Para iniciar o jogo desenvolvido com Pygame, execute o arquivo `main.py` localizado na pasta `games/pygame_game/`.

---

## 📜 Licença

Este projeto é licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.