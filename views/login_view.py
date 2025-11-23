import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuario_controller import UsuarioController

class TelaLogin(tk.Toplevel):
    def __init__(self, parent, callback_sucesso, on_logout):
        super().__init__(parent)
        self.callback_sucesso = callback_sucesso
        self.controlador = UsuarioController()
        self.on_logout = on_logout
        
        largura = 300
        altura = 260
        
        self.title("Login - Sistema CataVoo")
        self.geometry(f"{largura}x{altura}")
        self.resizable(False, False)
        
        # Centralização da janela
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (largura // 2)
        y = (screen_height // 2) - (altura // 2)
        self.geometry(f'{largura}x{altura}+{x}+{y}')

        self._criar_widgets()

        self.protocol("WM_DELETE_WINDOW", self.sair)

    def _criar_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=('Helvetica', 10))
        style.configure("TButton", font=('Helvetica', 10, 'bold'))
        
        main_frame = ttk.Frame(self, padding="30 20 30 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Campos de Login ---
        ttk.Label(main_frame, text="Login:").pack(anchor="w")
        self.login_entry = ttk.Entry(main_frame)
        self.login_entry.pack(fill="x", pady=(0, 10))
        self.login_entry.focus()

        ttk.Label(main_frame, text="Senha:").pack(anchor="w")
        self.senha_entry = ttk.Entry(main_frame, show="*")
        self.senha_entry.pack(fill="x", pady=(0, 20))
        
        self.senha_entry.bind('<Return>', lambda event: self.realizar_login())

        # --- Botão Entrar (Padrão) ---
        self.login_button = ttk.Button(main_frame, text="Entrar", command=self.realizar_login)
        self.login_button.pack(fill="x", pady=(0, 10)) # Adicionei espaço abaixo dele

        # Botão para sair
        tk.Button(
            main_frame, 
            text="Sair do Sistema", 
            command=self.sair, 
            bg="#ffcccc",
            fg="#cc0000",
            font=("Arial", 10, "bold"),
            height=2,
            relief="flat",
            cursor="hand2"
        ).pack(fill="x", side="bottom")

    def realizar_login(self):
        login = self.login_entry.get()
        senha = self.senha_entry.get()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        usuario = self.controlador.autenticar(login, senha)

        if usuario:
            self.destroy()
            self.callback_sucesso(usuario)
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos.")
            self.senha_entry.delete(0, 'end')
    
    def sair(self):
        if self.on_logout:
            self.on_logout()
        else:
            self.destroy()