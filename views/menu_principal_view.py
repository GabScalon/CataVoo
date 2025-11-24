import tkinter as tk
from views.uc03b_view import ViewCompanhia
from views.uc03a_view import ViewAeronave

class TelaMenu(tk.Frame):
    def __init__(self, parent, usuario, on_logout):
        super().__init__(parent)
        self.parent = parent
        self.on_logout = on_logout
        
        lbl_bemvindo = tk.Label(
            self, 
            text=f"Bem-vindo, {usuario.nome}!", 
            font=("Arial", 16, "bold")
        )
        lbl_bemvindo.pack(pady=(30, 5))
        
        lbl_tipo = tk.Label(
            self, 
            text=f"Perfil: {usuario.__class__.__name__}", 
            font=("Arial", 10), 
            fg="gray"
        )
        lbl_tipo.pack(pady=(0, 20))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10, fill='x', padx=50)

        btn_comp = tk.Button(
            btn_frame, 
            text="Gerenciar Companhias Aéreas", 
            command=self.abrir_companhias, 
            font=("Arial", 12),
            height=2
        )
        btn_comp.pack(fill='x', pady=5)

        btn_aero = tk.Button(
            btn_frame, 
            text="Gerenciar Aeronaves (Frota)", 
            command=self.abrir_aeronaves, 
            font=("Arial", 12),
            height=2
        )
        btn_aero.pack(fill='x', pady=5)

        tk.Button(
            self, 
            text="Sair do Sistema", 
            command=self.sair, 
            bg="#ffcccc", 
            fg="red"
        ).pack(side="bottom", pady=30)

    def abrir_companhias(self):
        """Abre a janela exclusiva de Companhias"""
        ViewCompanhia(self.parent)

    def abrir_aeronaves(self):
        """Abre a janela exclusiva de Aeronaves"""
        ViewAeronave(self.parent)

    def sair(self):
        """Chama a função de logout passada pelo main.py"""
        if self.on_logout:
            self.on_logout()