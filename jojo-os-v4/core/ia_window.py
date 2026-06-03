# ia_window.py
import tkinter as tk
from tkinter import scrolledtext
import os
from dotenv import load_dotenv
import threading

# IMPORTANTE: Importar a função que já corrigimos e que funciona!
from core.iagemini import perguntar_ia 
from ui.themes.jojo_theme import JoJoTheme

load_dotenv()

def abrir_janela_ia(app):
    janela_ia = tk.Toplevel(app.root)
    janela_ia.title("JOJO-OS // HEAVEN'S DOOR AI")
    janela_ia.geometry("700x600")
    janela_ia.configure(bg=JoJoTheme.BLACK)

    def executar_comando(texto):
        texto_lower = texto.lower()
        if "calculadora" in texto_lower or "calc" in texto_lower:
            app.open_calc()
            return "Abrindo calculadora..."
        if any(palavra in texto_lower for palavra in ("batalha", "battle", "lutar", "fight", "duel", "atacar")):
            app.open_battle()
            return "Preparando a batalha..."
        if "debugger" in texto_lower:
            app.open_debugger()
            return "Abrindo debugger..."
        return None

    # Título estilizado
    tk.Label(janela_ia, text="📖 HEAVEN'S DOOR", font=("Impact", 24), 
             bg=JoJoTheme.BLACK, fg=JoJoTheme.GOLD).pack(pady=10)

    chat_box = scrolledtext.ScrolledText(janela_ia, bg="#1A1A1A", fg=JoJoTheme.WHITE, 
                                        font=("Courier New", 12), wrap=tk.WORD,
                                        insertbackground=JoJoTheme.GOLD)
    chat_box.pack(padx=20, pady=10, fill="both", expand=True)
    chat_box.config(state=tk.DISABLED)

    entrada_usuario = tk.Entry(janela_ia, bg="#2A2A2A", fg=JoJoTheme.PINK, 
                              font=("Impact", 14), insertbackground=JoJoTheme.GOLD,
                              bd=3, relief="sunken")
    entrada_usuario.pack(padx=20, pady=10, fill="x")

    def enviar_mensagem():
        pergunta = entrada_usuario.get()
        if pergunta.strip():
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, f"👤 [JOJO]: {pergunta}\n", "user")
            chat_box.tag_config("user", foreground=JoJoTheme.PINK)
            entrada_usuario.delete(0, tk.END)
            
            # Mostra que a IA está "escrevendo"
            chat_box.insert(tk.END, "✒️ [HEAVEN'S DOOR]: Escrevendo...\n", "thinking")
            chat_box.tag_config("thinking", foreground="#555555")
            chat_box.config(state=tk.DISABLED)
            chat_box.see(tk.END)

            def atualizar_chat(texto):
                chat_box.config(state=tk.NORMAL)
                # Remove o "Escrevendo..."
                chat_box.delete("end-2l", "end-1l") 
                
                if "ERRO" in texto or "💥" in texto:
                    chat_box.insert(tk.END, f"{texto}\n\n", "error")
                    chat_box.tag_config("error", foreground="red")
                else:
                    chat_box.insert(tk.END, f"✒️ [HEAVEN'S DOOR]: {texto}\n\n", "ai")
                    chat_box.tag_config("ai", foreground=JoJoTheme.GOLD)
                
                chat_box.config(state=tk.DISABLED)
                chat_box.see(tk.END)

            comando_resposta = executar_comando(pergunta)
            if comando_resposta:
                atualizar_chat(comando_resposta)
                return

            def processar_ia():
                # USANDO A FUNÇÃO QUE JÁ TEM O MODELO CORRETO (2.0-flash)
                resposta = perguntar_ia(pergunta)
                
                # Atualiza a interface (precisa ser no thread principal)
                janela_ia.after(0, lambda: atualizar_chat(resposta))

            threading.Thread(target=processar_ia).start()

    btn_enviar = tk.Button(janela_ia, text="WRYYYYYYY! (ENVIAR)", command=enviar_mensagem, 
                          bg=JoJoTheme.PURPLE, fg=JoJoTheme.GOLD, font=("Impact", 14, "bold"),
                          activebackground=JoJoTheme.PINK, activeforeground=JoJoTheme.WHITE)
    btn_enviar.pack(pady=15)
    
    entrada_usuario.bind("<Return>", lambda e: enviar_mensagem())