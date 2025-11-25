import tkinter as tk
from views.companhia_view import ViewCompanhia
from views.aeronave_view import ViewAeronave
from views.administrador_view import AdministradorView
from views.voo_view import ViewVoo 
from views.piloto_view import ViewPiloto
from views.aeroporto_view import ViewAeroporto
from views.relatorio_view import RelatorioView

class TelaMenu(tk.Frame):
    def __init__(self, parent, usuario, controller, on_logout):
        super().__init__(parent)
        self.parent = parent
        self.usuario = usuario 
        self.controller = controller
        self.on_logout = on_logout
        
        # --- Labels de Cabeçalho ---
        lbl_bemvindo = tk.Label(self, text=f"Bem-vindo, {usuario.nome}!", font=("Arial", 16, "bold"))
        lbl_bemvindo.pack(pady=(30, 5))
        
        lbl_tipo = tk.Label(self, text=f"Perfil: {usuario.__class__.__name__}", font=("Arial", 10), fg="gray")
        lbl_tipo.pack(pady=(0, 20))

        # --- Frame dos Botões ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10, fill='x', padx=50)

        # ---------------------------------------------------------------------
        # ÁREA COMUM (Disponível para Funcionários e Admins)
        # ---------------------------------------------------------------------

        # BOTÃO DE VOOS (Painel Principal)
        btn_voos = tk.Button(
            btn_frame, 
            text="Gerenciar Voos (Painel Principal)", 
            command=self.abrir_voos, 
            font=("Arial", 12, "bold"),
            bg="#ddffdd", # Destaque verde
            height=2
        )
        btn_voos.pack(fill='x', pady=5)

        # ---------------------------------------------------------------------
        # ÁREA EXCLUSIVA DE ADMINISTRADOR
        # ---------------------------------------------------------------------
        if usuario.__class__.__name__ == 'Administrador':

            tk.Label(btn_frame, text="--- Administração ---", fg="gray").pack(pady=(10, 5))

            tk.Button(
                btn_frame, text="Gerenciar Companhias Aéreas", 
                command=self.abrir_companhias, font=("Arial", 12), height=2
            ).pack(fill='x', pady=5)

            tk.Button(
                btn_frame, text="Gerenciar Aeronaves (Frota)", 
                command=self.abrir_aeronaves, font=("Arial", 12), height=2
            ).pack(fill='x', pady=5)

            tk.Button(
                btn_frame, text="Gerenciar Aeroportos", 
                command=self.abrir_aeroportos, font=("Arial", 12), height=2
            ).pack(fill='x', pady=5)

            tk.Button(
                btn_frame, text="Gerenciar Pilotos", 
                command=self.abrir_pilotos, font=("Arial", 12), height=2
            ).pack(fill='x', pady=5)

            tk.Button(
                btn_frame,
                text="Gerenciar Usuários (Admin)",
                command=self.abrir_usuarios,
                font=("Arial", 12),
                height=2,
                bg="#e6f3ff"
            ).pack(fill='x', pady=5)

            tk.Button(
                btn_frame,
                text="Relatórios de Sistema (Logs)",
                command=self.abrir_relatorios,
                font=("Arial", 12),
                height=2,
                bg="#e6f3ff"
            ).pack(fill='x', pady=5)

        tk.Button(self, text="Sair do Sistema", command=self.sair, bg="#ffcccc", fg="red").pack(side="bottom", pady=30)

    def abrir_voos(self):
        """Abre a tela de voos passando o usuário logado."""
        ViewVoo(self.parent, self.usuario)

    def abrir_companhias(self):
        ViewCompanhia(self.parent)

    def abrir_aeronaves(self):
        ViewAeronave(self.parent)

    def abrir_aeroportos(self):
        ViewAeroporto(self.parent)

    def abrir_pilotos(self):
        ViewPiloto(self.parent)

    def abrir_usuarios(self):
        AdministradorView(self.parent, self.controller)

    def abrir_relatorios(self):
        RelatorioView(self.parent)

    def sair(self):
        if self.on_logout:
            self.on_logout()