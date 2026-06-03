import tkinter as tk
from core.stand_data import STANDS
from PIL import Image, ImageTk

class StandMenu:
    def __init__(self, master, callback):
        self.win = tk.Toplevel(master)
        self.win.title("Escolha seu Stand")
        self.win.geometry("600x500")
        self.win.configure(bg="black")

        self.callback = callback

        self.frame = tk.Frame(self.win, bg="black")
        self.frame.pack(fill="both", expand=True)

        for stand, data in STANDS.items():
            self.add_stand(stand, data)

    def add_stand(self, name, data):
        frame = tk.Frame(self.frame, bg="black", bd=2, relief="ridge")
        frame.pack(padx=10, pady=10, fill="x")

        try:
            img = Image.open(data["img"]).resize((80, 80))
            img = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(frame, image=img)
            lbl_img.image = img
            lbl_img.pack(side="left")
        except:
            pass

        info = tk.Frame(frame, bg="black")
        info.pack(side="left", padx=10)

        tk.Label(info, text=name, fg="gold", bg="black", font=("Impact", 14)).pack(anchor="w")
        tk.Label(info, text=data["bio"], fg="white", bg="black").pack(anchor="w")

        tk.Button(frame, text="Escolher",
                  command=lambda: self.select(name),
                  bg="purple", fg="gold").pack(side="right")

    def select(self, stand):
        self.callback(stand)
        self.win.destroy()