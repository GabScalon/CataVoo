import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from persistent.log_DAO import LogDAO

class RelatorioView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.dao = LogDAO()
        
        self.title("Relatório de Auditoria e Logs")
        self.geometry("900x500")
        self.transient(parent)

        self.__setup_ui()
        self.__carregar_logs()

    def __setup_ui(self):
        # Filtros
        frame_top = ttk.LabelFrame(self, text="Filtros", padding=10)
        frame_top.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_top, text="Buscar (Usuário/Voo):").pack(side='left')
        self.ent_busca = ttk.Entry(frame_top, width=20)
        self.ent_busca.pack(side='left', padx=5)

        ttk.Label(frame_top, text="Período:").pack(side='left', padx=(20, 5))
        self.combo_periodo = ttk.Combobox(frame_top, values=["Tudo", "Hoje", "Últimos 7 dias"], state="readonly")
        self.combo_periodo.set("Tudo")
        self.combo_periodo.pack(side='left')

        ttk.Button(frame_top, text="Filtrar", command=self.__carregar_logs).pack(side='left', padx=10)

        # Tabela
        cols = ('data', 'usuario', 'acao', 'alvo', 'detalhes')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        self.tree.heading('data', text='Data/Hora')
        self.tree.heading('usuario', text='Usuário Resp.')
        self.tree.heading('acao', text='Ação')
        self.tree.heading('alvo', text='Alvo')
        self.tree.heading('detalhes', text='Detalhes')

        self.tree.column('data', width=120)
        self.tree.column('usuario', width=100)
        self.tree.column('acao', width=100)
        self.tree.column('alvo', width=80)
        self.tree.column('detalhes', width=300)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def __carregar_logs(self):
        # Limpar tabela
        for i in self.tree.get_children():
            self.tree.delete(i)

        termo = self.ent_busca.get()
        periodo = self.combo_periodo.get()
        
        data_inicio = None
        if periodo == "Hoje":
            data_inicio = datetime.now().replace(hour=0, minute=0, second=0)
        elif periodo == "Últimos 7 dias":
            data_inicio = datetime.now() - timedelta(days=7)

        # Busca no DAO
        logs = self.dao.buscar_por_filtro(termo, data_inicio)

        for log in logs:
            self.tree.insert('', 'end', values=(
                log.data_hora.strftime("%d/%m/%Y %H:%M"),
                log.usuario_responsavel,
                log.acao,
                log.alvo,
                log.detalhes
            ))