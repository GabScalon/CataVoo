import tkinter as tk
from views.companhia_view import ViewCompanhia
from views.aeronave_view import ViewAeronave
from views.administrador_view import AdministradorView
# 1. IMPORTAR A NOVA VIEW
from views.voo_view import ViewVoo 

class TelaMenu(tk.Frame):
    def __init__(self, parent, usuario, controller, on_logout):
        super().__init__(parent)
        self.parent = parent
        self.usuario = usuario # Importante: Guardamos o usuário aqui
        self.controller = controller
        self.on_logout = on_logout
        
        # --- Labels de Cabeçalho ---
        lbl_bemvindo = tk.Label(self, text=f"Bem-vindo, {usuario.nome}!", font=("Arial", 16, "bold"))
        lbl_bemvindo.pack(pady=(30, 5))
        
        lbl_tipo = tk.Label(self, text=f"Perfil: {usuario.__class__.__name__}", font=("Arial", 10), fg="gray")
        lbl_tipo.pack(pady=(0, 20))

        # --- Botões ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10, fill='x', padx=50)

        # 2. BOTÃO DE VOOS (NOVO)
        # Colocamos em primeiro pois é a função principal do sistema
        btn_voos = tk.Button(
            btn_frame, 
            text="Gerenciar Voos (Painel Principal)", 
            command=self.abrir_voos, 
            font=("Arial", 12, "bold"),
            bg="#ddffdd", # Um verde claro para destacar
            height=2
        )
        btn_voos.pack(fill='x', pady=5)

        btn_comp = tk.Button(
            btn_frame, text="Gerenciar Companhias Aéreas", 
            command=self.abrir_companhias, font=("Arial", 12), height=2
        )
        btn_comp.pack(fill='x', pady=5)

        btn_aero = tk.Button(
            btn_frame, text="Gerenciar Aeronaves (Frota)", 
            command=self.abrir_aeronaves, font=("Arial", 12), height=2
        )
        btn_aero.pack(fill='x', pady=5)

        # Botão Usuários (Apenas Admin)
        if usuario.__class__.__name__ == 'Administrador':
            btn_users = tk.Button(
                btn_frame,
                text="Gerenciar Usuários (Admin)",
                command=self.abrir_usuarios,
                font=("Arial", 12),
                height=2,
                bg="#e6f3ff"
            )
            btn_users.pack(fill='x', pady=5)

        tk.Button(self, text="Sair do Sistema", command=self.sair, bg="#ffcccc", fg="red").pack(side="bottom", pady=30)

    def abrir_companhias(self):
        ViewCompanhia(self.parent)

    def abrir_aeronaves(self):
        ViewAeronave(self.parent)

    def abrir_usuarios(self):
        AdministradorView(self.parent, self.controller)

    # 3. MÉTODO PARA ABRIR VOOS
    def abrir_voos(self):
        """
        Abre a tela de voos passando o usuário logado.
        A própria ViewVoo vai decidir se habilita os botões de edição
        baseado nesse usuário.
        """
        ViewVoo(self.parent, self.usuario)

    def sair(self):
        if self.on_logout:
            self.on_logout()