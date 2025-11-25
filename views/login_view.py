import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class TelaLogin(tk.Toplevel):
    def __init__(self, parent, controller, callback_sucesso, on_logout=None):
        super().__init__(parent)
        self.controller = controller
        self.callback_sucesso = callback_sucesso
        self.on_logout = on_logout
        
        self.title("Login - CataVoo")
        self.geometry("300x250")
        self.protocol("WM_DELETE_WINDOW", self.sair)
        
        # Centralizar
        x = (self.winfo_screenwidth() // 2) - 150
        y = (self.winfo_screenheight() // 2) - 125
        self.geometry(f'+{x}+{y}')

        self._criar_widgets()

    def _criar_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Login:").pack(anchor='w')
        self.ent_login = ttk.Entry(frame)
        self.ent_login.pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame, text="Senha:").pack(anchor='w')
        self.ent_senha = ttk.Entry(frame, show="*")
        self.ent_senha.pack(fill='x', pady=(0, 20))
        
        self.ent_senha.bind('<Return>', lambda e: self.fazer_login())
        
        ttk.Button(frame, text="Entrar", command=self.fazer_login).pack(fill='x')
        tk.Button(frame, text="Sair", command=self.sair, fg="red", relief="flat").pack(fill='x', pady=10)

    def fazer_login(self):
        login = self.ent_login.get()
        senha = self.ent_senha.get()
        
        usuario = self.controller.autenticar(login, senha)
        
        if not usuario:
            messagebox.showerror("Erro", "Credenciais inválidas.")
            return
            
        # Lógica de Primeiro Acesso
        if usuario.primeiro_acesso:
            messagebox.showinfo("Bem-vindo", "Primeiro acesso detectado.\nVocê deve definir uma nova senha.")
            nova_senha = simpledialog.askstring("Definir Senha", "Nova Senha:", show='*', parent=self)
            
            if nova_senha:
                if self.controller.definir_nova_senha(usuario.cpf, nova_senha):
                    messagebox.showinfo("Sucesso", "Senha atualizada! Entrando...")
                    usuario.confirmar_primeiro_acesso()
                else:
                    messagebox.showerror("Erro", "Falha ao atualizar senha.")
                    return
            else:
                return

        self.destroy()
        self.callback_sucesso(usuario)

    def sair(self):
        if self.on_logout: self.on_logout()
        else: self.destroy()