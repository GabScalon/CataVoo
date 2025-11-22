import tkinter as tk
from tkinter import ttk, messagebox
from controller import ControladorCompanhia, ControladorAeronave

# Tela Principal (Menu)
class TelaGerenciamento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        parent.title("Menu de Gerenciamento")
        parent.geometry("300x200")

        lbl_titulo = tk.Label(self, text="Opções de Gerenciamento", font=("Arial", 14))
        lbl_titulo.pack(pady=20)

        btn_ger_companhia = tk.Button(self, text="Gerenciar Companhias Aéreas",
                                      command=self.abrir_ger_companhias, width=30)
        btn_ger_companhia.pack(pady=10)

        btn_ger_aeronave = tk.Button(self, text="Gerenciar Modelos de Aeronave",
                                     command=self.abrir_ger_aeronaves, width=30)
        btn_ger_aeronave.pack(pady=10)

    def abrir_ger_companhias(self):
        TelaCRUD(self.parent, "Gerenciar Companhias", ControladorCompanhia())

    def abrir_ger_aeronaves(self):
        TelaCRUD(self.parent, "Gerenciar Aeronaves", ControladorAeronave())

# Tela Genérica de CRUD
class TelaCRUD(tk.Toplevel):
    def __init__(self, parent, titulo, controlador):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title(titulo)
        self.geometry("600x400")

        self.controlador = controlador
        self.is_companhia = isinstance(self.controlador, ControladorCompanhia)

        self._criar_widgets()
        self.atualizar_lista()

    def _criar_widgets(self):
        frm_botoes = tk.Frame(self)
        frm_botoes.pack(fill='x', padx=10, pady=10)

        btn_cadastrar = tk.Button(frm_botoes, text="Cadastrar Novo", command=self.clicarCadastrarNova)
        btn_cadastrar.pack(side='left', padx=5)

        btn_editar = tk.Button(frm_botoes, text="Editar Selecionado", command=self.abrir_formulario_edicao)
        btn_editar.pack(side='left', padx=5)

        btn_excluir = tk.Button(frm_botoes, text="Excluir Selecionado", command=self.excluir_item)
        btn_excluir.pack(side='left', padx=5)

        cols = ('id', 'nome', 'extra')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome/Modelo')
        self.tree.heading('extra', text='Email/Companhia')

        self.tree.column('id', width=50, stretch=False)
        self.tree.column('nome', width=200)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if self.is_companhia:
            lista = self.controlador.get_all_companhias()
            for item in lista:
                self.tree.insert('', 'end', values=(item.id, item.nome, item.email))
        else:
            companhias = {c.id: c.nome for c in self.controlador.get_all_companhias()}
            lista = self.controlador.get_all_aeronaves()
            for item in lista:
                nome_comp = companhias.get(item.companhia_id, "ID não encontrado")
                self.tree.insert('', 'end', values=(item.id, item.modelo, nome_comp))

    def _get_id_selecionado(self):
        try:
            selecionado = self.tree.focus()
            if not selecionado:
                raise Exception("Nenhum item selecionado.")
            item = self.tree.item(selecionado)
            return item['values'][0]
        except Exception as e:
            messagebox.showwarning("Atenção", str(e), parent=self)
            return None

    def clicarCadastrarNova(self):
        self.exibirFormularioCadastro()

    def exibirFormularioCadastro(self):
        if self.is_companhia:
            FormularioCompanhia(self, self.controlador, self.atualizar_lista)
        else:
            FormularioAeronave(self, self.controlador, self.atualizar_lista)

    def abrir_formulario_edicao(self):
        item_id = self._get_id_selecionado()
        if not item_id:
            return

        if self.is_companhia:
            item_para_editar = self.controlador.companhia_dao.get_by_id(item_id)
            FormularioCompanhia(self, self.controlador, self.atualizar_lista, item_para_editar)
        else:
            item_para_editar = self.controlador.aeronave_dao.get_by_id(item_id)
            FormularioAeronave(self, self.controlador, self.atualizar_lista, item_para_editar)

    def excluir_item(self):
        item_id = self._get_id_selecionado()
        if not item_id:
            return

        if not messagebox.askyesno("Confirmar Exclusão",
                                   "Tem certeza que deseja excluir este item?",
                                   parent=self):
            return

        sucesso, msg = self.controlador.excluir(item_id)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.atualizar_lista()
        else:
            messagebox.showerror("Erro de Exclusão", msg, parent=self)


# Formulário de Cadastro/Edição de COMPANHIA
class FormularioCompanhia(tk.Toplevel):
    def __init__(self, parent, controlador, callback_atualizar, companhia=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("Cadastrar Nova Companhia" if not companhia else "Editar Companhia")
        self.geometry("400x450")

        self.controlador = controlador
        self.callback = callback_atualizar
        self.companhia = companhia
        self.entries = {}

        self._criar_formulario()
        if self.companhia:
            self._preencher_formulario()

    def _criar_campo(self, frame, label_text):
        frm_campo = tk.Frame(frame)
        frm_campo.pack(fill='x', padx=5, pady=5)
        lbl = tk.Label(frm_campo, text=label_text, width=20, anchor='w')
        lbl.pack(side='left')
        entry = tk.Entry(frm_campo, width=30)
        entry.pack(side='left', fill='x', expand=True)
        return entry

    def _criar_formulario(self):
        frm_principal = tk.Frame(self)
        frm_principal.pack(fill='both', expand=True, padx=15, pady=15)

        lbl_comp = tk.Label(frm_principal, text="Dados da Companhia", font=("Arial", 12, "bold"))
        lbl_comp.pack(pady=5)
        self.entries['nome'] = self._criar_campo(frm_principal, "Nome *")
        self.entries['email'] = self._criar_campo(frm_principal, "Email")
        self.entries['numeroContato'] = self._criar_campo(frm_principal, "Contato")

        lbl_endereco = tk.Label(frm_principal, text="Endereço da Sede", font=("Arial", 12, "bold"))
        lbl_endereco.pack(pady=10)
        self.entries['rua'] = self._criar_campo(frm_principal, "Rua *")
        self.entries['numero'] = self._criar_campo(frm_principal, "Número")
        self.entries['bairro'] = self._criar_campo(frm_principal, "Bairro")
        self.entries['cidade'] = self._criar_campo(frm_principal, "Cidade *")
        self.entries['estado'] = self._criar_campo(frm_principal, "Estado")
        self.entries['pais'] = self._criar_campo(frm_principal, "País")

        btn_salvar = tk.Button(frm_principal, text="Salvar", command=self.salvar)
        btn_salvar.pack(pady=20)

    def _preencher_formulario(self):
        if not self.companhia:
            return

        self.entries['nome'].insert(0, self.companhia.nome)
        self.entries['email'].insert(0, self.companhia.email)
        self.entries['numeroContato'].insert(0, self.companhia.numeroContato)

        if self.companhia.enderecoSede:
            end = self.companhia.enderecoSede
            self.entries['rua'].insert(0, end.rua)
            self.entries['numero'].insert(0, end.numero)
            self.entries['bairro'].insert(0, end.bairro)
            self.entries['cidade'].insert(0, end.cidade)
            self.entries['estado'].insert(0, end.estado)
            self.entries['pais'].insert(0, end.pais)

    def operacaoSucesso(self, msg):
        self.exibirMensagemSucesso(msg)
        self.exibirOpcoesGerenciamento()

    def exibirMensagemSucesso(self, msg):
        messagebox.showinfo("Sucesso", msg, parent=self)
    
    def erroValidacao(self, msg):
        self.exibirMensagemErro(msg)

    def exibirMensagemErro(self, msg):
        messagebox.showerror("Erro de Validação", msg, parent=self)

    def exibirOpcoesGerenciamento(self):
        self.callback()
        self.destroy()

    def salvar(self):
        dadosCompanhia = {
            'nome': self.entries['nome'].get(),
            'email': self.entries['email'].get(),
            'numeroContato': self.entries['numeroContato'].get(),
        }
        dadosEndereco = {
            'rua': self.entries['rua'].get(),
            'numero': self.entries['numero'].get(),
            'bairro': self.entries['bairro'].get(),
            'cidade': self.entries['cidade'].get(),
            'estado': self.entries['estado'].get(),
            'pais': self.entries['pais'].get(),
        }

        if self.companhia:
            sucesso, msg = self.controlador.atualizar(
                self.companhia.id, dadosCompanhia, dadosEndereco)
        else:
            sucesso, msg = self.controlador.cadastrar(dadosCompanhia, dadosEndereco)

        # Tratamento do Retorno (Linhas tracejadas do diagrama)
        if sucesso:
            self.operacaoSucesso(msg)
        else:
            self.erroValidacao(msg)


# Formulário de Cadastro/Edição de AERONAVE
class FormularioAeronave(tk.Toplevel):
    def __init__(self, parent, controlador, callback_atualizar, aeronave=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("Cadastrar Nova Aeronave" if not aeronave else "Editar Aeronave")
        self.geometry("400x300")

        self.controlador = controlador
        self.callback = callback_atualizar
        self.aeronave = aeronave
        self.entries = {}

        self.companhias = self.controlador.get_all_companhias()
        self.map_comp_id_nome = {c.id: c.nome for c in self.companhias}
        self.map_comp_nome_id = {c.nome: c.id for c in self.companhias}

        self._criar_formulario()
        if self.aeronave:
            self._preencher_formulario()

    def _criar_campo(self, frame, label_text):
        frm_campo = tk.Frame(frame)
        frm_campo.pack(fill='x', padx=5, pady=5)
        lbl = tk.Label(frm_campo, text=label_text, width=20, anchor='w')
        lbl.pack(side='left')
        entry = tk.Entry(frm_campo, width=30)
        entry.pack(side='left', fill='x', expand=True)
        return entry

    def _criar_formulario(self):
        frm_principal = tk.Frame(self)
        frm_principal.pack(fill='both', expand=True, padx=15, pady=15)

        lbl_dados = tk.Label(frm_principal, text="Dados da Aeronave", font=("Arial", 12, "bold"))
        lbl_dados.pack(pady=5)

        frm_combo = tk.Frame(frm_principal)
        frm_combo.pack(fill='x', padx=5, pady=5)
        lbl_combo = tk.Label(frm_combo, text="Companhia *", width=20, anchor='w')
        lbl_combo.pack(side='left')
        self.combo_comp = ttk.Combobox(frm_combo,
                                          values=list(self.map_comp_nome_id.keys()),
                                          state="readonly", width=28)
        self.combo_comp.pack(side='left', fill='x', expand=True)

        self.entries['modelo'] = self._criar_campo(frm_principal, "Modelo *")
        self.entries['tipoDeAviao'] = self._criar_campo(frm_principal, "Tipo de Avião")
        self.entries['lotacaoMaxima'] = self._criar_campo(frm_principal, "Lotação Máxima")
        self.entries['capacidadeDeCarga'] = self._criar_campo(frm_principal, "Capacidade Carga (kg)")

        btn_salvar = tk.Button(frm_principal, text="Salvar", command=self.salvar)
        btn_salvar.pack(pady=20)

    def _preencher_formulario(self):
        if not self.aeronave:
            return

        self.entries['modelo'].insert(0, self.aeronave.modelo)
        self.entries['tipoDeAviao'].insert(0, self.aeronave.tipoDeAviao)
        self.entries['lotacaoMaxima'].insert(0, self.aeronave.lotacaoMaxima)
        self.entries['capacidadeDeCarga'].insert(0, self.aeronave.capacidadeDeCarga)

        nome_comp = self.map_comp_id_nome.get(self.aeronave.companhia_id)
        if nome_comp:
            self.combo_comp.set(nome_comp)

    def operacaoSucesso(self, msg):
        self.exibirMensagemSucesso(msg)
        self.exibirOpcoesGerenciamento()

    def exibirMensagemSucesso(self, msg):
        messagebox.showinfo("Sucesso", msg, parent=self)

    def erroValidacao(self, msg):
        self.exibirMensagemErro(msg)

    def exibirMensagemErro(self, msg):
        messagebox.showerror("Erro de Validação", msg, parent=self)

    def exibirOpcoesGerenciamento(self):
        self.callback()
        self.destroy()

    def salvar(self):
        nome_comp_selecionada = self.combo_comp.get()
        companhia_id = self.map_comp_nome_id.get(nome_comp_selecionada)

        dadosAeronave = {
            'modelo': self.entries['modelo'].get(),
            'companhia_id': companhia_id, 
            'tipoDeAviao': self.entries['tipoDeAviao'].get(),
            'lotacaoMaxima': self.entries['lotacaoMaxima'].get(),
            'capacidadeDeCarga': self.entries['capacidadeDeCarga'].get(),
        }

        if self.aeronave:
            sucesso, msg = self.controlador.atualizar(self.aeronave.id, dadosAeronave)
        else:
            sucesso, msg = self.controlador.cadastrar(dadosAeronave)

        if sucesso:
            self.operacaoSucesso(msg)
        else:
            self.erroValidacao(msg)