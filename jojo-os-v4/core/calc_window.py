# calc_window.py
import tkinter as tk
from ui.themes.jojo_theme import JoJoTheme
from ui.themes.hacker_theme import HackerTheme
import os
from pygame import mixer 
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageGrab

def localizar_pasta_soms():
    """Busca a pasta 'soms' subindo os níveis de diretório até encontrar"""
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        tentativa = os.path.join(diretorio_atual, "soms")
        if os.path.exists(tentativa): 
            return tentativa
        diretorio_atual = os.path.dirname(diretorio_atual)
    return None

class JoJoCalc:
    def __init__(self, master, theme_atual="JOJO", sound_mode="ora"):
        self.sound_mode = sound_mode
        self.master = master
        # Define o tema com base na escolha do sistema
        self.theme_name = theme_atual
        self.theme = JoJoTheme if theme_atual == "JOJO" else HackerTheme
        
        self.master.title("JOJO CALCULATOR" if theme_atual == "JOJO" else "CLEITAN-OS TERMINAL")
        self.master.geometry("400x600")
        self.master.configure(bg="#000000") # Fundo sempre preto para ambos

        self.system_root = self.master.winfo_toplevel()
        
        # Configuração de sons e estados
        self.hold_job = None 
        self.was_held = False 
        self.ee_activated = False 

        # Definição de cores de Inversão (Efeito Especial)
        if theme_atual == "JOJO":
            self.neg_black, self.neg_gold = "#ffffff", "#005aff"
            self.neg_purple, self.neg_pink = "#a0ff5f", "#00ffbf"
            self.text_color = "#FFD700" # Dourado JoJo
        else:
            # Cores "Matrix" para o modo Hacker
            self.neg_black, self.neg_gold = "#000000", "#00FF41"
            self.neg_purple, self.neg_pink = "#003B00", "#008F11"
            self.text_color = "#00FF00" # Verde Hacker

        self.canvas_overlay = None
        self.radius = 0

        # Inicialização de Sons
        try:
            mixer.init()
            pasta = localizar_pasta_soms()
            if self.sound_mode == "muda":
                # DIO
                self.click_sound = mixer.Sound(os.path.join(pasta, "inutil.wav"))
                self.hold_sound = mixer.Sound(os.path.join(pasta, "dio-time-stop.wav"))
            else:
                # JOTARO
                self.click_sound = mixer.Sound(os.path.join(pasta, "ora-jotaro.wav"))
                self.hold_sound = mixer.Sound(os.path.join(pasta, "star-platinum-zw.wav"))
        except:
            self.click_sound = None
            self.hold_sound = None    
        self.result_var = tk.StringVar()
        self.buttons_list = [] 
        self.create_widgets()

    def play_sound(self, sound_type):
        try:
            mixer.stop() # PARA o som anterior para não bugar
            if sound_type == "click" and self.click_sound: self.click_sound.play()
            elif sound_type == "hold" and self.hold_sound: self.hold_sound.play()
        except: pass

    def stop_time_effect(self):
        if self.ee_activated: return
        self.ee_activated = True
        self.was_held = True # Marca que foi um clique longo
        self.play_sound("hold")

        x, y = self.system_root.winfo_rootx(), self.system_root.winfo_rooty()
        w, h = self.system_root.winfo_width(), self.system_root.winfo_height()

        try:
            self.canvas_overlay = tk.Canvas(self.system_root, bg="black")
            self.canvas_overlay.place(relwidth=1, relheight=1)

            self.canvas_overlay.create_text(
                w//2, h//2,
                text="ZA WARUDO",
                fill="white",
                font=("Impact", 50)
            )
            
            self.canvas_overlay = tk.Canvas(self.system_root, width=w, height=h, highlightthickness=0)
            self.canvas_overlay.place(x=0, y=0)

            # 👇 força atualização
            self.system_root.update_idletasks()
            self.canvas_overlay.lift()

            self.radius = 10
            self.animate_expansion(w, h)
            # CAPTURA DA TELA
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            img = ImageOps.invert(img.convert("RGB"))

            self.overlay_image = img
        except:
            self.ee_activated = False

    def animate_expansion(self, w, h):
        max_radius = (w**2 + h**2)**0.5
        if self.radius < max_radius:
            self.radius += 60 # Velocidade da expansão
            mask = Image.new('L', (w, h), 0)
            draw = ImageDraw.Draw(mask)
            cx, cy = w // 2, h // 2
            draw.ellipse((cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius), fill=255)
            
            current_frame = Image.new('RGBA', (w, h), (0,0,0,0))
            current_frame.paste(self.overlay_image, (0, 0), mask=mask)
            
            self.inverted_tk = ImageTk.PhotoImage(current_frame)
            self.canvas_overlay.delete("all")
            self.canvas_overlay.create_image(0, 0, image=self.inverted_tk, anchor="nw")
            self.master.after(15, lambda: self.animate_expansion(w, h))
        else:
            self.apply_negative_ui()
            self.master.after(3000, self.restore_colors)

    def apply_negative_ui(self):
        self.master.configure(bg=self.neg_black)
        self.display.configure(bg="#e5e5e5", fg=self.neg_gold)
        for btn, char in self.buttons_list:
            neg_bg = self.neg_purple if char.isdigit() else self.neg_pink
            btn.configure(bg=neg_bg, fg=self.neg_black)

    def restore_colors(self):
        if self.canvas_overlay:
            self.canvas_overlay.delete("all")
            self.canvas_overlay.destroy()
            self.canvas_overlay = None
        
        # Volta as cores originais do tema
        self.master.configure(bg="#000000")
        self.display.configure(bg="#1a1a1a", fg=self.text_color)
        for btn, char in self.buttons_list:
            orig_bg = self.theme.PURPLE if char.isdigit() else self.theme.PINK
            btn.configure(bg=orig_bg, fg=self.text_color)
        self.ee_activated = False

    def on_press(self, char):
        self.was_held = False
        # Se segurar por mais de 400ms, ativa o ZA WARUNDO / HACK
        self.hold_job = self.master.after(400, self.stop_time_effect)

    def on_release(self, char):
        if self.hold_job:
            self.master.after_cancel(self.hold_job)
            self.hold_job = None
        
        if not self.was_held:
            if char == 'C': self.result_var.set("")
            elif char == '=':
                try: 
                    res = str(eval(self.result_var.get()))
                    self.result_var.set(res)
                except: self.result_var.set("ERROR")
            else: 
                self.result_var.set(self.result_var.get() + char)
            self.play_sound("click")

    def create_widgets(self):
        font_name = "Impact" if self.theme_name == "JOJO" else "Courier New"
        
        self.display = tk.Entry(self.master, textvariable=self.result_var, font=(font_name, 32), 
                           bg="#1a1a1a", fg=self.text_color, bd=5, relief="sunken", justify='right')
        self.display.pack(expand=True, fill='both', padx=10, pady=10)

        btn_frame = tk.Frame(self.master, bg="#000000")
        btn_frame.pack(expand=True, fill='both', padx=5, pady=5)

        btns = ['7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', 'C', '=', '+']
        r, c = 0, 0
        for b in btns:
            try:
                if b.isdigit():
                    color = getattr(self.theme, 'PURPLE', "#003b00")
                else:
                    color = getattr(self.theme, 'PINK', "#008f11")
            except:
                color = "#1a1a1a" # Cor de segurança caso tudo falhe
            
            btn = tk.Button(btn_frame, text=b, font=(font_name, 20), 
                            bg=color, fg=self.text_color,
                            activebackground=self.text_color, activeforeground="black",
                            relief="raised" if self.theme_name == "JOJO" else "flat")
            
            # Binds para clique longo e curto
            btn.bind("<ButtonPress-1>", lambda e, b=b: self.on_press(b))
            btn.bind("<ButtonRelease-1>", lambda e, b=b: self.on_release(b))
            
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
            self.buttons_list.append((btn, b))
            
            c += 1
            if c > 3: 
                c = 0
                r += 1
        
        for i in range(4): 
            btn_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            btn_frame.grid_rowconfigure(i, weight=1)

# Função para testar a janela sozinha
if __name__ == "__main__":
    root = tk.Tk()
    app = JoJoCalc(root, theme_atual="HACKER") # Teste manual
    root.mainloop()