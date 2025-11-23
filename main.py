import tkinter as tk
from views.login_view import TelaLogin
from views.menu_view import TelaMenu
from controllers.usuario_controller import UsuarioController

# Import necessário apenas para criar o admin inicial se o banco estiver vazio
from entities.administrador import Administrador

def verificar_setup_inicial():
    #  Verifica se o banco de usuários está vazio, se estiver, cria o usuário 'admin' padrão.
    controller = UsuarioController()
    usuarios = controller.buscar_todos()
    
    if not usuarios:
        print("--- Banco de usuários vazio. Criando ADMIN padrão... ---")
        # Cria o Admin
        dados_admin = {
            'nome': 'Administrador Geral',
            'login': 'admin',
            'senha': '123', 
            'cpf': '000.000.000-00',
            'aeroporto_id': 0
        }
        controller.cadastrar(dados_admin, eh_admin=True)
        
        # Cria um funcionário comum para teste
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
        
        # Garante que existam usuários antes de abrir a tela
        verificar_setup_inicial()
        
        # Oculta a janela principal enquanto o login acontece
        self.withdraw() 
        
        # Inicia o fluxo de Login
        self.mostrar_login()

    def mostrar_login(self):
        """Abre a janela de login (Toplevel)."""
        login_window = TelaLogin(self, callback_sucesso=self.login_sucesso)
        # Bloqueia a interação com outras janelas até fechar o login
        login_window.wait_window() 

    def login_sucesso(self, usuario):
        """Chamado quando o login é bem-sucedido."""
        self.deiconify() # Mostra a janela principal (Root)
        self.usuario_logado = usuario
        
        # Limpa widgets anteriores (se houver logout)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame): # Remove frames antigos
                widget.destroy()

        # Carrega o Menu Principal
        menu = TelaMenu(self, usuario, on_logout=self.fazer_logout)
        menu.pack(fill="both", expand=True)

    def fazer_logout(self):
        """Reseta a aplicação para a tela de login."""
        self.withdraw() # Esconde a janela principal
        self.mostrar_login() # Mostra login novamente

if __name__ == "__main__":
    app = App()
    app.mainloop()