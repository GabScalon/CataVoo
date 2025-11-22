import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import os
from typing import Dict, Optional

# --- Modelos de Dados ---

class Usuario:
    """Representa um usuário do sistema."""
    def __init__(self, login: str, senha: str, nome: str, tipo: str):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.tipo = tipo

    def __repr__(self):
        return f"Usuario(nome='{self.nome}', tipo='{self.tipo}')"

# --- Persistência de Dados (Pickle) ---

ARQUIVO_DADOS = "usuarios.pkl"

def carregar_dados() -> Dict[str, Usuario]:
    """
    Carrega o dicionário de usuários de um arquivo pickle.
    Retorna um dicionário vazio se o arquivo não for encontrado.
    """
    try:
        with open(ARQUIVO_DADOS, 'rb') as f:
            print(f"Carregando dados de '{ARQUIVO_DADOS}'...")
            return pickle.load(f)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os dados: {e}")
        return {}

def salvar_dados(db: Dict[str, Usuario]):
    """Salva o dicionário de usuários em um arquivo pickle."""
    try:
        with open(ARQUIVO_DADOS, 'wb') as f:
            pickle.dump(db, f)
            print(f"Dados salvos com sucesso em '{ARQUIVO_DADOS}'.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")

# --- Lógica do Caso de Uso ---

def autenticar_usuario(login: str, senha: str, db: Dict[str, Usuario]) -> Optional[Usuario]:
    """
    [UC02] Verifica as credenciais de um usuário.
    Retorna o objeto Usuario se a autenticação for bem-sucedida, senão None.
    
    Args:
        login (str): O login a ser verificado.
        senha (str): A senha a ser verificada.
        db (Dict[str, Usuario]): O "banco de dados" de usuários.
    """
    print(f"--- [UC02] Tentando autenticar usuário: {login} ---")
    usuario = db.get(login)
    if usuario and usuario.senha == senha:
        print(f"Autenticação bem-sucedida para {usuario.nome}.")
        return usuario
    
    print("Falha na autenticação: login ou senha inválidos.")
    return None

# --- Interface Gráfica (GUI com Tkinter) ---

class TelaLogin:
    def __init__(self, master, db_usuarios):
        self.master = master
        self.db_usuarios = db_usuarios
        self.master.title("Login - Sistema de Autenticação")
        self.master.geometry("300x150") # Define o tamanho da janela

        # Estilo
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("TButton", padding=5, font=('Helvetica', 10, 'bold'))
        style.configure("TEntry", padding=5, font=('Helvetica', 10))
        
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Widgets
        ttk.Label(main_frame, text="Login:").grid(row=0, column=0, sticky="w")
        self.login_entry = ttk.Entry(main_frame)
        self.login_entry.grid(row=0, column=1, sticky="ew")
        # Focar no campo de login ao iniciar
        self.login_entry.focus()

        ttk.Label(main_frame, text="Senha:").grid(row=1, column=0, sticky="w")
        self.senha_entry = ttk.Entry(main_frame, show="*") # Oculta a senha
        self.senha_entry.grid(row=1, column=1, sticky="ew")

        self.login_button = ttk.Button(main_frame, text="Entrar", command=self.realizar_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar expansão das colunas
        main_frame.columnconfigure(1, weight=1)

    def realizar_login(self):
        """Pega os dados dos inputs e chama a função de autenticação."""
        login = self.login_entry.get()
        senha = self.senha_entry.get()

        if not login or not senha:
            messagebox.showwarning("Entrada Inválida", "Por favor, preencha ambos os campos.")
            return

        usuario_autenticado = autenticar_usuario(login, senha, self.db_usuarios)

        if usuario_autenticado:
            messagebox.showinfo(
                "Login Bem-Sucedido",
                f"Bem-vindo, {usuario_autenticado.nome}!\nTipo de Acesso: {usuario_autenticado.tipo}"
            )
            self.master.destroy()  # Fecha a janela de login após sucesso
        else:
            messagebox.showerror("Falha na Autenticação", "Login ou senha inválidos.")
            # Limpa o campo de senha para nova tentativa
            self.senha_entry.delete(0, 'end')


# --- Execução Principal ---

if __name__ == "__main__":
    # 1. Verifica se o arquivo de dados existe. Se não, cria com dados de exemplo.
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"Arquivo '{ARQUIVO_DADOS}' não encontrado. Criando com dados de exemplo...")
        db_inicial = {
            "admin": Usuario("admin", "senha123", "Admin Geral", "Administrador"),
            "func1": Usuario("func1", "funcsenha", "João Silva", "Funcionário"),
        }
        salvar_dados(db_inicial)

    # 2. Carrega os dados dos usuários do arquivo
    db_usuarios_carregado = carregar_dados()

    # 3. Inicia a interface gráfica
    root = tk.Tk()
    app = TelaLogin(root, db_usuarios_carregado)
    root.mainloop()
