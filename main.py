import tkinter as tk
from views.uc01_view import TelaLogin
from views.menu_principal_view import TelaMenu
from controllers.usuario_controller import UsuarioController
from entities.administrador import Administrador

def verificar_setup_inicial():
    controller = UsuarioController()
    usuarios = controller.buscar_todos()
    
    if not usuarios:
        print("--- Banco de usuários vazio. Criando ADMIN padrão... ---")
        dados_admin = {
            'nome': 'Administrador Geral',
            'login': 'admin',
            'senha': '123', 
            'cpf': '000.000.000-00',
            'aeroporto_id': 0
        }
        controller.cadastrar(dados_admin, eh_admin=True)
        
        dados_func = {
            'nome': 'João Silva',
            'login': 'func',
            'senha': '123'
        }
        controller.cadastrar(dados_func, eh_admin=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema CataVoo")
        self.geometry("800x600")
        
        verificar_setup_inicial()
        
        self.withdraw() 
        self.mostrar_login()

    def mostrar_login(self):
        """Abre a janela de login."""
        login_window = TelaLogin(
            self, 
            callback_sucesso=self.login_sucesso, 
            on_logout=self.destroy
        )
        login_window.wait_window() 

    def login_sucesso(self, usuario):
        self.deiconify() 
        self.usuario_logado = usuario
        
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        menu = TelaMenu(self, usuario, on_logout=self.fazer_logout)
        menu.pack(fill="both", expand=True)

    def fazer_logout(self):
        self.withdraw()
        self.mostrar_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()