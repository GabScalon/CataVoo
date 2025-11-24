import tkinter as tk
from persistent import UsuarioRepository
from controllers.usuario_controller import UsuarioController
from views.login_view import TelaLogin
from views.menu_view import TelaMenu
from model.dto import CadastroUsuarioDTO

def verificar_setup_inicial(controller):
    """
    Verifica se o banco de dados está vazio.
    Se estiver, cria um usuário ADMINISTRADOR padrão.
    """
    # Usa o método público do controller (sem acessar atributos privados com __)
    usuarios = controller.listar_todos()
    
    if not usuarios:
        print("--- SETUP INICIAL: Banco de dados vazio. ---")
        print("--- Criando Administrador Padrão... ---")
        
        # Cria o DTO. Nota: Não passamos senha, pois o sistema gera baseada no CPF.
        dto = CadastroUsuarioDTO(
            cpf="000.000.000-00",
            nome="Super Administrador",
            email="admin@sistema.com",
            login="admin",
            tipo_usuario="ADMINISTRADOR"
        )
        
        status, msg = controller.cadastrar_usuario(dto)
        
        print(msg)
        print("------------------------------------------------")
        print("DADOS PARA PRIMEIRO ACESSO:")
        print("Login: admin")
        print("Senha: 00000000000 (Números do CPF)")
        print("------------------------------------------------")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema CataVoo")
        self.geometry("800x600")
        
        # ---------------------------------------------------------
        # 1. INJEÇÃO DE DEPENDÊNCIA (O "Cérebro" do sistema)
        # Criamos o Repositório e o Controller aqui. Eles ficam vivos
        # durante toda a execução do programa.
        # ---------------------------------------------------------
        self.repository = UsuarioRepository("persistent/dados/db_usuarios.pkl")
        self.controller = UsuarioController(self.repository)

        # Roda a verificação antes de mostrar qualquer tela
        verificar_setup_inicial(self.controller)
        
        # Esconde a janela principal e abre o login
        self.withdraw() 
        self.mostrar_login()

    def mostrar_login(self):
        """Abre a janela de login passando o controller."""
        TelaLogin(
            self, 
            controller=self.controller, 
            callback_sucesso=self.login_sucesso, 
            on_logout=self.destroy
        )

    def login_sucesso(self, usuario):
        """Chamado quando o login é realizado com sucesso."""
        self.deiconify() # Mostra a janela principal
        self.usuario_logado = usuario
        
        # Remove qualquer widget anterior (limpeza da tela)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        # Cria o Menu Principal
        # IMPORTANTE: Passamos o 'self.controller' para o Menu,
        # para que ele possa abrir a tela de Gerenciar Usuários depois.
        menu = TelaMenu(
            parent=self, 
            usuario=usuario, 
            controller=self.controller, # <--- Passando a ferramenta
            on_logout=self.fazer_logout
        )
        menu.pack(fill="both", expand=True)

    def fazer_logout(self):
        """Esconde o menu e volta para o login."""
        self.withdraw()
        self.mostrar_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()