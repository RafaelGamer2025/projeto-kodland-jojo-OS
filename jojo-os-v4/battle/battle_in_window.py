import tkinter as tk
import random
import os

from pygame import mixer

from core.battle_system import criar_lutador
from battle.attack_cards import ATTACKS


class BattleWindow:

    def __init__(self, master, user, player_stand):

        # =========================================
        # JANELA
        # =========================================

        self.win = tk.Toplevel(master)

        self.win.title("⚔️ STAND BATTLE")

        self.win.geometry("1100x750")

        self.win.configure(bg="black")

        # =========================================
        # PLAYER / ENEMY
        # =========================================

        self.player = criar_lutador(player_stand)

        self.enemy = criar_lutador("The World")

        # =========================================
        # CONTROLE DE BATALHA
        # =========================================

        self.turno = "player"

        self.enemy_stunned = False

        # =========================================
        # SISTEMA DE TEMPO
        # =========================================

        self.current_second = 1

        self.max_seconds = 7

        self.attacks_used = 0

        self.max_attacks = 3

        # =========================================
        # COMBO
        # =========================================

        self.combo = []

        self.win.bind("<Up>", self.combo_input)

        self.win.bind("<Down>", self.combo_input)

        self.win.bind("<KeyPress-p>", self.combo_input)

        # =========================================
        # TÍTULO
        # =========================================

        tk.Label(
            self.win,
            text="⚔️ STAND BATTLE SYSTEM ⚔️",
            fg="gold",
            bg="black",
            font=("Impact", 26)
        ).pack(pady=10)

        # =========================================
        # TEMPO
        # =========================================

        self.time_label = tk.Label(
            self.win,
            text="⏳ TEMPO: 1",
            fg="cyan",
            bg="black",
            font=("Impact", 22)
        )

        self.time_label.pack()

        # =========================================
        # ESCOLHER INIMIGO
        # =========================================

        enemy_frame = tk.Frame(
            self.win,
            bg="black"
        )

        enemy_frame.pack(pady=10)

        tk.Label(
            enemy_frame,
            text="👤 ESCOLHA O INIMIGO",
            fg="gold",
            bg="black",
            font=("Impact", 14)
        ).pack()

        # =========================================
        # SCROLL
        # =========================================

        scroll = tk.Scrollbar(enemy_frame)

        scroll.pack(
            side="right",
            fill="y"
        )

        self.enemy_listbox = tk.Listbox(
            enemy_frame,
            height=6,
            width=30,
            bg="#111",
            fg="white",
            font=("Impact", 12),
            yscrollcommand=scroll.set
        )

        self.enemy_listbox.pack()

        scroll.config(
            command=self.enemy_listbox.yview
        )

        # =========================================
        # STANDS
        # =========================================

        stands = list(ATTACKS.keys())

        for stand in stands:

            self.enemy_listbox.insert(
                "end",
                stand
            )

        self.enemy_listbox.selection_set(0)

        # =========================================
        # BOTÃO TROCAR INIMIGO
        # =========================================

        tk.Button(
            enemy_frame,
            text="⚔️ SELECIONAR",
            bg="purple",
            fg="gold",
            font=("Impact", 12),
            command=self.trocar_inimigo
        ).pack(pady=5)

        # =========================================
        # HP
        # =========================================

        self.hp_label = tk.Label(
            self.win,
            text="",
            fg="white",
            bg="black",
            font=("Impact", 16)
        )

        self.hp_label.pack(pady=10)

        # =========================================
        # STAND GAUGE
        # =========================================

        self.special_points = 0

        self.gauge = tk.Label(
            self.win,
            text="STAND GAUGE: 0%",
            fg="cyan",
            bg="black",
            font=("Impact", 14)
        )

        self.gauge.pack()

        self.special_btn = tk.Button(
            self.win,
            text="🔥 SPECIAL",
            bg="gray",
            fg="white",
            state="disabled",
            font=("Impact", 14),
            command=self.usar_especial
        )

        self.special_btn.pack(pady=5)

        # =========================================
        # LOG
        # =========================================

        self.log = tk.Text(
            self.win,
            bg="#111",
            fg="gold",
            font=("Courier New", 11),
            height=18
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================================
        # CORES
        # =========================================

        self.log.tag_config(
            "player",
            foreground="lime"
        )

        self.log.tag_config(
            "enemy",
            foreground="red"
        )

        self.log.tag_config(
            "special",
            foreground="cyan"
        )

        self.log.tag_config(
            "win",
            foreground="gold"
        )

        self.log.tag_config(
            "lose",
            foreground="red"
        )

        self.log.tag_config(
            "time",
            foreground="orange"
        )

        # =========================================
        # CARDS
        # =========================================

        self.cards_frame = tk.Frame(
            self.win,
            bg="black"
        )

        self.cards_frame.pack(pady=10)

        self.render_cards()

        self.atualizar_hp()

        # =========================================
        # INICIAR TIMER
        # =========================================

        self.start_timer()

    # =====================================================
    # TIMER
    # =====================================================

    def start_timer(self):

        if self.player["hp"] <= 0:
            return

        if self.enemy["hp"] <= 0:
            return

        self.time_label.config(
            text=f"⏳ TEMPO: {self.current_second}"
        )

        self.current_second += 1

        # =========================
        # ACABOU O TEMPO
        # =========================

        if self.current_second > self.max_seconds:

            self.current_second = 1

            self.attacks_used = 0

            self.turno = "enemy"

            self.enemy_turn()

        self.win.after(
            1000,
            self.start_timer
        )

    # =====================================================
    # RENDER CARDS
    # =====================================================

    def render_cards(self):

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        deck = ATTACKS[self.player["stand"]]

        cards = random.sample(
            deck,
            min(3, len(deck))
        )

        for attack in cards:

            crit = False

            dano = attack["dano"]

            # =========================
            # CRIT RNG
            # =========================

            if random.randint(1, 100) >= 85:

                crit = True

                dano *= 2

            texto = (
                f"{attack['nome']}\n"
                f"DMG {dano}"
            )

            if crit:
                texto += "\n💥 CRIT"

            btn = tk.Button(
                self.cards_frame,
                text=texto,
                bg=attack["cor"],
                fg="black",
                width=20,
                height=6,
                bd=5,
                relief="raised",
                cursor="hand2",
                font=("Impact", 10),
                command=lambda a=attack, d=dano:
                    self.player_attack(a, d)
            )

            btn.pack(
                side="left",
                padx=8
            )

    # =====================================================
    # PLAYER ATTACK
    # =====================================================

    def player_attack(self, attack, dano):

        # =========================
        # NÃO É SEU TURNO
        # =========================

        if self.turno != "player":
            return

        # =========================
        # LIMITE
        # =========================

        if self.attacks_used >= self.max_attacks:

            self.log.insert(
                "end",
                "\n⛔ LIMITE DE ATAQUES!\n",
                "time"
            )

            return

        self.attacks_used += 1

        # =========================
        # DANO
        # =========================

        self.enemy["hp"] -= dano

        self.log.insert(
            "end",
            f"\n⚔️ {attack['nome']} causou {dano}!\n",
            "player"
        )

        efeito = attack["efeito"]

        # =========================
        # EFEITOS
        # =========================

        if efeito == "timestop":

            self.enemy_stunned = True

            self.log.insert(
                "end",
                "🕒 ZA WARUDO!\n",
                "special"
            )

            self.flash_screen("#AAAAAA")

            self.play_sound("time_stop.wav")

        elif efeito == "rotation":

            self.anim_rotation()

        elif efeito == "reflect":

            self.anim_love_train()

        elif efeito == "bomb":

            extra = random.randint(5, 20)

            self.enemy["hp"] -= extra

            self.log.insert(
                "end",
                f"💣 EXPLOSÃO EXTRA {extra}\n",
                "special"
            )

        elif efeito == "curse":

            curse = random.randint(10, 25)

            self.enemy["hp"] -= curse

            self.log.insert(
                "end",
                f"☠️ CALAMITY {curse}\n",
                "special"
            )

        # =========================
        # SONS
        # =========================

        if self.player["stand"] == "Star Platinum":

            self.play_sound("ora.wav")

        elif self.player["stand"] == "The World":

            self.play_sound("muda.wav")

        # =========================
        # STAND GAUGE
        # =========================

        self.special_points += random.randint(15, 30)

        if self.special_points > 100:
            self.special_points = 100

        self.gauge.config(
            text=f"STAND GAUGE: {self.special_points}%"
        )

        # =========================
        # LIBERA ESPECIAL
        # =========================

        if self.special_points >= 100:

            self.special_btn.config(
                state="normal",
                bg="gold",
                fg="black"
            )

        self.atualizar_hp()

        self.check_finish()

        self.render_cards()

    # =====================================================
    # IA INIMIGA
    # =====================================================

    def enemy_turn(self):

        if self.enemy["hp"] <= 0:
            return

        # =========================
        # ZA WARUDO
        # =========================

        if self.enemy_stunned:

            self.log.insert(
                "end",
                "\n🕒 INIMIGO PARADO NO TEMPO!\n",
                "special"
            )

            self.enemy_stunned = False

            self.turno = "player"

            return

        enemy_deck = ATTACKS[self.enemy["stand"]]

        attack = random.choice(enemy_deck)

        dano = attack["dano"]

        self.player["hp"] -= dano

        self.log.insert(
            "end",
            f"\n☠️ {self.enemy['stand']} usou {attack['nome']}!\n",
            "enemy"
        )

        self.log.insert(
            "end",
            f"💥 Você recebeu {dano} de dano!\n",
            "enemy"
        )

        self.atualizar_hp()

        self.check_finish()

        self.turno = "player"

    # =====================================================
    # ESPECIAL
    # =====================================================

    def usar_especial(self):

        if self.special_points < 100:
            return

        self.special_points = 0

        self.gauge.config(
            text="STAND GAUGE: 0%"
        )

        self.special_btn.config(
            state="disabled",
            bg="gray"
        )

        dano = random.randint(40, 70)

        self.enemy["hp"] -= dano

        self.log.insert(
            "end",
            f"\n🔥 SPECIAL causou {dano}\n",
            "special"
        )

        self.atualizar_hp()

        self.check_finish()

    # =====================================================
    # TROCAR INIMIGO
    # =====================================================

    def trocar_inimigo(self):

        selecionado = self.enemy_listbox.curselection()

        if not selecionado:
            return

        stand = self.enemy_listbox.get(
            selecionado[0]
        )

        self.enemy = criar_lutador(stand)

        self.log.insert(
            "end",
            f"\n👤 NOVO INIMIGO: {stand}\n",
            "special"
        )

        self.log.see("end")

        self.atualizar_hp()

    # =====================================================
    # COMBO
    # =====================================================

    def combo_input(self, event):

        tecla = event.keysym.lower()

        self.combo.append(tecla)

        if len(self.combo) > 5:
            self.combo.pop(0)

        segredo = [
            "up",
            "up",
            "down",
            "down",
            "p"
        ]

        if self.combo == segredo:

            self.enemy["hp"] -= 50

            self.log.insert(
                "end",
                "\n🌟 COMBO SECRETO!\n",
                "special"
            )

            self.atualizar_hp()

            self.combo.clear()

    # =====================================================
    # HP
    # =====================================================

    def atualizar_hp(self):

        self.hp_label.config(
            text=(
                f"{self.player['stand']} HP: {self.player['hp']}        "
                f"{self.enemy['stand']} HP: {self.enemy['hp']}"
            )
        )

    # =====================================================
    # FINAL
    # =====================================================

    def check_finish(self):

        if self.enemy["hp"] <= 0:

            self.log.insert(
                "end",
                "\n🏆 VOCÊ VENCEU!\n",
                "win"
            )

        elif self.player["hp"] <= 0:

            self.log.insert(
                "end",
                "\n💀 VOCÊ PERDEU!\n",
                "lose"
            )

    # =====================================================
    # FLASH
    # =====================================================

    def flash_screen(self, color):

        original = self.win["bg"]

        self.win.configure(bg=color)

        self.win.after(
            200,
            lambda: self.win.configure(bg=original)
        )

    # =====================================================
    # SOM
    # =====================================================

    def play_sound(self, file):

        try:

            mixer.Sound(
                os.path.join(
                    "soms",
                    file
                )
            ).play()

        except Exception as e:

            print(e)

    # =====================================================
    # ROTATION
    # =====================================================

    def anim_rotation(self):

        overlay = tk.Toplevel(self.win)

        overlay.attributes("-fullscreen", True)

        overlay.configure(bg="black")

        tk.Label(
            overlay,
            text="🌀 INFINITE ROTATION 🌀",
            fg="cyan",
            bg="black",
            font=("Impact", 55)
        ).pack(expand=True)

        self.win.after(
            1200,
            overlay.destroy
        )

    # =====================================================
    # LOVE TRAIN
    # =====================================================

    def anim_love_train(self):

        overlay = tk.Toplevel(self.win)

        overlay.attributes("-fullscreen", True)

        overlay.configure(bg="yellow")

        tk.Label(
            overlay,
            text="🌈 LOVE TRAIN 🌈",
            fg="black",
            bg="yellow",
            font=("Impact", 60)
        ).pack(expand=True)

        self.win.after(
            1200,
            overlay.destroy
        )