import tkinter as tk
import winsound

class PopupAutoClose:
    def __init__(self, mensagem, tempo_fechar=3000):  # Tempo em milissegundos (3 segundos padrão)
        self.root = tk.Tk()
        self.root.withdraw()  # Esconde a janela principal
        self.root.title("Popup")
        self.root.geometry("300x150")  # Ajusta o tamanho da janela

        self.label = tk.Label(self.root, text=mensagem, font=("Arial", 12))
        self.label.pack(padx=10, pady=10)

        # Configura um temporizador para fechar a janela após um tempo específico
        self.root.after(tempo_fechar, self.fechar_popup)

    def fechar_popup(self):
        self.root.destroy()

    def exibir(self):
        # Toca o som do sistema (substitua 'path/do/seu/som.wav' pelo caminho do seu arquivo de som)
        winsound.PlaySound('path/do/seu/som.wav', winsound.SND_FILENAME)

        # Centraliza a janela na tela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

        self.root.deiconify()  # Torna a janela visível
        self.root.mainloop()

# Exemplo de uso
mensagem = "Esta é uma mensagem de popup que desaparecerá após 3 segundos."
popup = PopupAutoClose(mensagem)
popup.exibir()
