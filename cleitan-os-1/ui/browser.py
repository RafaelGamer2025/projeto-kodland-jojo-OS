import tkinter as tk
import webbrowser

class BrowserApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Navegador Estilo Hacker")
        self.master.geometry("800x600")
        self.master.configure(bg="#0a0a0a")

        self.url_entry = tk.Entry(self.master, width=50, bg="#1a1a1a", fg="#00ff00", font=("Courier", 12))
        self.url_entry.pack(pady=20)

        self.go_button = tk.Button(self.master, text="Ir", command=self.open_browser, bg="#1a1a1a", fg="#00ff00", font=("Courier", 12))
        self.go_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Sair", command=self.master.quit, bg="#1a1a1a", fg="#ff0000", font=("Courier", 12))
        self.quit_button.pack(pady=10)

    def open_browser(self):
        url = self.url_entry.get()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrowserApp(root)
    root.mainloop()