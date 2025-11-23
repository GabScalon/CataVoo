import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class TelaLogin(tk.Toplevel):
    def __init__(self, parent, callback_sucesso):
        """
        :param parent: Janela pai (root)
        :param callback_sucesso: Função para chamar quando o login der certo (ex: abrir menu)
        """
        super().__init__(parent)
        self.callback_sucesso = callback_sucesso
        self.controlador = UsuarioController()
        
        self.title("Login - Sistema CataVoo")
        self.geometry("300x180")
        self.resizable(False, False)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self._criar_widgets()

    def _criar_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=('Helvetica', 10))
        style.configure("TButton", font=('Helvetica', 10, 'bold'))
        
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Login
        ttk.Label(main_frame, text="Login:").pack(anchor="w")
        self.login_entry = ttk.Entry(main_frame)
        self.login_entry.pack(fill="x", pady=(0, 10))
        self.login_entry.focus()

        # Senha
        ttk.Label(main_frame, text="Senha:").pack(anchor="w")
        self.senha_entry = ttk.Entry(main_frame, show="*")
        self.senha_entry.pack(fill="x", pady=(0, 20))
        
        # Bind da tecla Enter para clicar no botão
        self.senha_entry.bind('<Return>', lambda event: self.realizar_login())

        # Botão
        self.login_button = ttk.Button(main_frame, text="Entrar", command=self.realizar_login)
        self.login_button.pack(fill="x")

    def realizar_login(self):
        login = self.login_entry.get()
        senha = self.senha_entry.get()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        # Chama o controlador (MVC)
        usuario = self.controlador.autenticar(login, senha)

        if usuario:
            # Se sucesso, fecha esta janela e chama o callback (Menu)
            self.destroy()
            self.callback_sucesso(usuario)
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos.")
            self.senha_entry.delete(0, 'end')