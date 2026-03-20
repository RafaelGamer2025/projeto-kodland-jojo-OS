# filepath: c:\Users\Rafael\OneDrive\Anexos\Área de Trabalho\site\cleitan-os\core\calc_window.py
import tkinter as tk

class HackerCalc:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora Hacker")
        self.master.geometry("400x600")
        self.master.configure(bg="#0a0a0a")

        self.result_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Display
        display = tk.Entry(self.master, textvariable=self.result_var, font=("Courier", 24), bg="#1a1a1a", fg="#00ff00", bd=0, justify='right')
        display.pack(expand=True, fill='both')

        # Buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(expand=True, fill='both')

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row_val = 0
        col_val = 0

        for button in buttons:
            btn = tk.Button(button_frame, text=button, font=("Courier", 18), bg="#0a0a0a", fg="#00ff00", bd=0, command=lambda b=button: self.on_button_click(b))
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.result_var.set("")
        elif char == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Error")
        else:
            current_text = self.result_var.get()
            self.result_var.set(current_text + char)