import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.voo_controller import VooController
from model.administrador import Administrador 

class ViewVoo(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.controller = VooController()
        
        self.title("Gerenciamento de Voos")
        self.geometry("1000x600")
        self.transient(parent)

        self.map_aeroportos = {}
        self.map_aeronaves = {}
        self.map_companhias = {}
        self.map_pilotos = {}

        self.__setup_ui()
        self.__carregar_dados()

    def __setup_ui(self):
        # --- Frame de Busca ---
        frame_busca = ttk.LabelFrame(self, text="Filtros", padding=10)
        frame_busca.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_busca, text="Buscar por:").pack(side='left')
        self.var_tipo_busca = tk.StringVar(value="CODIGO")
        ttk.Radiobutton(frame_busca, text="Código", variable=self.var_tipo_busca, value="CODIGO").pack(side='left', padx=5)
        ttk.Radiobutton(frame_busca, text="Destino (ID Aeroporto)", variable=self.var_tipo_busca, value="DESTINO").pack(side='left', padx=5)

        self.entry_busca = ttk.Entry(frame_busca, width=30)
        self.entry_busca.pack(side='left', padx=5)
        ttk.Button(frame_busca, text="Buscar", command=self.__realizar_busca).pack(side='left')
        ttk.Button(frame_busca, text="Limpar/Atualizar", command=self.__carregar_dados).pack(side='left', padx=5)

        # --- Treeview (Lista de Voos) ---
        colunas = ('id', 'codigo', 'origem', 'destino', 'partida', 'chegada', 'status', 'passageiros')
        self.tree = ttk.Treeview(self, columns=colunas, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('codigo', text='Código')
        self.tree.heading('origem', text='Origem (ID)')
        self.tree.heading('destino', text='Destino (ID)')
        self.tree.heading('partida', text='Partida Prev.')
        self.tree.heading('chegada', text='Chegada Prev.')
        self.tree.heading('status', text='Status')
        self.tree.heading('passageiros', text='Pax')

        self.tree.column('id', width=30)
        self.tree.column('codigo', width=80)
        self.tree.column('status', width=100)
        self.tree.column('passageiros', width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='top', fill='both', expand=True, padx=10, pady=5)
        scrollbar.pack(side='right', fill='y')

        # --- Frame de Ações ---
        frame_acoes = ttk.Frame(self, padding=10)
        frame_acoes.pack(fill='x', side='bottom')

        # Verificação de Permissão: ADMIN
        eh_admin = isinstance(self.usuario, Administrador) or self.usuario.__class__.__name__ == 'Administrador'

        self.btn_novo = ttk.Button(frame_acoes, text="Novo Voo", command=self.__abrir_formulario_novo)
        self.btn_editar = ttk.Button(frame_acoes, text="Editar Dados", command=self.__abrir_formulario_edicao)
        self.btn_excluir = ttk.Button(frame_acoes, text="Excluir Voo", command=self.__excluir_voo)
        
        # Botão comum a todos
        self.btn_status = ttk.Button(frame_acoes, text="Alterar Status", command=self.__abrir_alterar_status)

        self.btn_novo.pack(side='left', padx=5)
        self.btn_editar.pack(side='left', padx=5)
        self.btn_excluir.pack(side='left', padx=5)
        
        # Separador visual
        ttk.Separator(frame_acoes, orient='vertical').pack(side='left', fill='y', padx=10)
        self.btn_status.pack(side='left', padx=5)

        # Lógica visual de permissão
        if not eh_admin:
            self.btn_novo.config(state='disabled')
            self.btn_editar.config(state='disabled')
            self.btn_excluir.config(state='disabled')

    def __carregar_dados(self):
        # Limpa tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Busca dados
        voos = self.controller.buscar_todos()
        
        for v in voos:
            # Formata data para string legível na grid
            partida_str = v.horarioDePartidaPrevisto.strftime("%d/%m/%Y %H:%M") if isinstance(v.horarioDePartidaPrevisto, datetime) else str(v.horarioDePartidaPrevisto)
            chegada_str = v.horarioDeChegadaPrevisto.strftime("%d/%m/%Y %H:%M") if isinstance(v.horarioDeChegadaPrevisto, datetime) else str(v.horarioDeChegadaPrevisto)

            self.tree.insert('', 'end', values=(
                v.id,
                v.codigo,
                v.localDeSaida_id,
                v.destino_id,
                partida_str,
                chegada_str,
                v.statusDoVoo,
                v.numeroDePassageiros
            ))

    def __realizar_busca(self):
        termo = self.entry_busca.get()
        if not termo:
            return self.__carregar_dados()

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if self.var_tipo_busca.get() == "CODIGO":
                resultados = self.controller.buscar_por_codigo(termo)
            else:
                resultados = self.controller.buscar_por_destino(int(termo))

            for v in resultados:
                partida_str = v.horarioDePartidaPrevisto.strftime("%d/%m/%Y %H:%M")
                chegada_str = v.horarioDeChegadaPrevisto.strftime("%d/%m/%Y %H:%M")
                self.tree.insert('', 'end', values=(v.id, v.codigo, v.localDeSaida_id, v.destino_id, partida_str, chegada_str, v.statusDoVoo, v.numeroDePassageiros))
        except ValueError:
            messagebox.showerror("Erro", "Para buscar por destino, digite o ID numérico do aeroporto.")

    # --------------------------------------------------------------------------
    # Lógica de Formulário (Cadastro/Edição) - Apenas Admin
    # --------------------------------------------------------------------------
    def __carregar_combos_dados(self):
        """Busca dados auxiliares no controller para preencher Comboboxes"""
        # Aeroportos (Nome -> ID)
        aeros = self.controller.get_aeroportos_para_combo()
        self.map_aeroportos = {f"{a.nome} (ID {a.id})": a.id for a in aeros}
        
        # Aeronaves (Correção: Removida matricula)
        naves = self.controller.get_aeronaves_para_combo()
        self.map_aeronaves = {f"{n.modelo} (ID {n.id})": n.id for n in naves}

        # Companhias
        comps = self.controller.get_companhias_para_combo()
        self.map_companhias = {f"{c.nome} (ID {c.id})": c.id for c in comps}

        # Pilotos (Correção: Usando codigoDeLicensa)
        pils = self.controller.get_pilotos_para_combo()
        self.map_pilotos = {f"{p.nome} - Licença: {p.codigoDeLicensa} (ID {p.id})": p.id for p in pils}

    def __abrir_formulario_novo(self):
        self.__abrir_janela_formulario("Novo Voo")

    def __abrir_formulario_edicao(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um voo para editar.")
            return
        
        valores = self.tree.item(item_selecionado[0], 'values')
        id_voo = int(valores[0])
        
        # Pega o objeto completo do banco para preencher todos os campos
        voo_completo = self.controller.voo_dao.get_by_id(id_voo)
        
        self.__abrir_janela_formulario("Editar Voo", voo_completo)

    def __abrir_janela_formulario(self, titulo, voo=None):
        self.__carregar_combos_dados()
        
        top = tk.Toplevel(self)
        top.title(titulo)
        top.geometry("600x600")
        top.transient(self)

        frame = ttk.Frame(top, padding=20)
        frame.pack(fill='both', expand=True)

        # Código
        self.ent_codigo = ttk.Entry(frame)
        self._criar_campo(frame, "Código:", self.ent_codigo)
        
        # Aeronave
        ttk.Label(frame, text="Aeronave:").pack(anchor='w')
        self.cb_aeronave = ttk.Combobox(frame, values=list(self.map_aeronaves.keys()), state="readonly")
        self.cb_aeronave.pack(fill='x', pady=2)

        # Companhia
        ttk.Label(frame, text="Companhia:").pack(anchor='w')
        self.cb_companhia = ttk.Combobox(frame, values=list(self.map_companhias.keys()), state="readonly")
        self.cb_companhia.pack(fill='x', pady=2)

        # Piloto
        ttk.Label(frame, text="Piloto:").pack(anchor='w')
        self.cb_piloto = ttk.Combobox(frame, values=list(self.map_pilotos.keys()), state="readonly")
        self.cb_piloto.pack(fill='x', pady=2)

        # Origem
        ttk.Label(frame, text="Origem:").pack(anchor='w')
        self.cb_origem = ttk.Combobox(frame, values=list(self.map_aeroportos.keys()), state="readonly")
        self.cb_origem.pack(fill='x', pady=2)

        # Destino
        ttk.Label(frame, text="Destino:").pack(anchor='w')
        self.cb_destino = ttk.Combobox(frame, values=list(self.map_aeroportos.keys()), state="readonly")
        self.cb_destino.pack(fill='x', pady=2)

        # Partida
        self.ent_partida = ttk.Entry(frame)
        self._criar_campo(frame, "Partida (dd/mm/aaaa HH:MM):", self.ent_partida)

        # Chegada
        self.ent_chegada = ttk.Entry(frame)
        self._criar_campo(frame, "Chegada (dd/mm/aaaa HH:MM):", self.ent_chegada)

        # Passageiros
        self.ent_pax = ttk.Entry(frame)
        self._criar_campo(frame, "Passageiros:", self.ent_pax)

        # Portão
        self.ent_portao = ttk.Entry(frame)
        self._criar_campo(frame, "Portão:", self.ent_portao)

        # Carga
        self.ent_carga = ttk.Entry(frame)
        self._criar_campo(frame, "Carga (Kg):", self.ent_carga)

        # Preencher dados se for edição
        if voo:
            self.ent_codigo.insert(0, voo.codigo)
            self.ent_pax.insert(0, str(voo.numeroDePassageiros))
            self.ent_portao.insert(0, voo.portao)
            self.ent_carga.insert(0, str(voo.carga))
            
            # Datas
            data_partida = voo.horarioDePartidaPrevisto.strftime("%d/%m/%Y %H:%M") if isinstance(voo.horarioDePartidaPrevisto, datetime) else str(voo.horarioDePartidaPrevisto)
            data_chegada = voo.horarioDeChegadaPrevisto.strftime("%d/%m/%Y %H:%M") if isinstance(voo.horarioDeChegadaPrevisto, datetime) else str(voo.horarioDeChegadaPrevisto)
            
            self.ent_partida.insert(0, data_partida)
            self.ent_chegada.insert(0, data_chegada)

            # Selecionar Combos (Reverse lookup nos mapas)
            self._set_combo(self.cb_aeronave, self.map_aeronaves, voo.aeronave_id)
            self._set_combo(self.cb_companhia, self.map_companhias, voo.companhia_id)
            self._set_combo(self.cb_piloto, self.map_pilotos, voo.piloto_id)
            self._set_combo(self.cb_origem, self.map_aeroportos, voo.localDeSaida_id)
            self._set_combo(self.cb_destino, self.map_aeroportos, voo.destino_id)

        # Botão Salvar
        btn_salvar = ttk.Button(frame, text="Salvar Voo", 
            command=lambda: self.__salvar_voo(top, voo.id if voo else None))
        btn_salvar.pack(pady=20, fill='x')

    def _criar_campo(self, parent, texto, entry):
        ttk.Label(parent, text=texto).pack(anchor='w')
        entry.pack(fill='x', pady=(0, 5))

    def _set_combo(self, combo, map_dict, id_alvo):
        """Seleciona o item no combobox baseado no ID"""
        for texto, id_val in map_dict.items():
            if id_val == id_alvo:
                combo.set(texto)
                return

    def __salvar_voo(self, janela, id_voo=None):
        try:
            # Conversão de Datas
            formato = "%d/%m/%Y %H:%M"
            partida_dt = datetime.strptime(self.ent_partida.get(), formato)
            chegada_dt = datetime.strptime(self.ent_chegada.get(), formato)
            
            # Montar Dicionário
            dados = {
                'codigo': self.ent_codigo.get(),
                'aeronave_id': self.map_aeronaves[self.cb_aeronave.get()],
                'companhia_id': self.map_companhias[self.cb_companhia.get()],
                'piloto_id': self.map_pilotos[self.cb_piloto.get()],
                'localDeSaida_id': self.map_aeroportos[self.cb_origem.get()],
                'destino_id': self.map_aeroportos[self.cb_destino.get()],
                'horarioDePartidaPrevisto': partida_dt,
                'horarioDeChegadaPrevisto': chegada_dt,
                'numeroDePassageiros': self.ent_pax.get(),
                'portao': self.ent_portao.get(),
                'carga': self.ent_carga.get(),
                'statusDoVoo': 'Programado' if not id_voo else None 
            }

            if id_voo:
                res, msg = self.controller.atualizar(id_voo, dados, self.usuario)
            else:
                res, msg = self.controller.cadastrar(dados, self.usuario)

            if res:
                messagebox.showinfo("Sucesso", msg)
                janela.destroy()
                self.__carregar_dados()
            else:
                messagebox.showerror("Erro", msg)

        except KeyError:
            messagebox.showwarning("Campos vazios", "Selecione todos os itens das listas (Aeronave, Aeroportos, etc).")
        except ValueError as e:
            messagebox.showerror("Erro de Formato", f"Verifique as datas (dd/mm/aaaa HH:MM) e números.\nErro: {e}")

    def __excluir_voo(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado: return
        
        id_voo = int(self.tree.item(item_selecionado[0], 'values')[0])
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este voo?"):
            sucesso, msg = self.controller.excluir(id_voo, self.usuario)
            messagebox.showinfo("Info", msg)
            if sucesso: self.__carregar_dados()

    def __abrir_alterar_status(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um voo para alterar o status.")
            return
        
        valores = self.tree.item(item_selecionado[0], 'values')
        id_voo = int(valores[0])
        status_atual = valores[6]

        janela = tk.Toplevel(self)
        janela.title("Atualizar Status")
        janela.geometry("300x150")
        
        ttk.Label(janela, text=f"Voo: {valores[1]}").pack(pady=10)
        ttk.Label(janela, text=f"Status Atual: {status_atual}").pack()
        
        status_opcoes = ["Programado", "Embarcando", "Cancelado", "Atrasado", "Realizado", "Voando"]
        combo_status = ttk.Combobox(janela, values=status_opcoes, state="readonly")
        combo_status.pack(pady=10)
        combo_status.set(status_atual)

        def confirmar():
            novo = combo_status.get()
            sucesso, msg = self.controller.alterar_status(id_voo, novo, self.usuario)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.__carregar_dados()
                janela.destroy()
            else:
                messagebox.showerror("Erro", msg)

        ttk.Button(janela, text="Confirmar", command=confirmar).pack(pady=5)