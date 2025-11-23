import tkinter as tk
from views.menu_view import TelaMenu
# from views.login_view import TelaLogin (Implementar depois)

# Mock de um usuário para teste rápido sem login
class UsuarioTeste:
    nome = "Administrador Teste"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema CataVoo")
    root.geometry("600x500")

    # Simula o login efetuado mostrando direto o menu
    # No sistema real, chamaria TelaLogin primeiro
    app = TelaMenu(root, UsuarioTeste(), on_logout=root.destroy)
    app.pack(fill="both", expand=True)

    root.mainloop()