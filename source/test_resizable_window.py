import tkinter as tk

root = tk.Tk()
root.title("Janela Mínima")
root.geometry("200x150")
root.resizable(True, True) # Garante que a janela seja redimensionável

tk.Label(root, text="Janela de Teste").pack(padx=20, pady=20)

root.mainloop()