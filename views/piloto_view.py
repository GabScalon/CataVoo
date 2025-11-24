import tkinter as tk
from tkinter import ttk, messagebox
from controllers.piloto_controller import PilotoController

class ViewPiloto(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Pilotos")
        self.geometry("700x450")
        self.transient(parent)
        self.grab_set()

        self.controlador = PilotoController()
        
        self._criar_widgets()
        self.atualizar_lista()

    def _criar_widgets(self):
        # Botões de Ação
        frm_botoes = tk.Frame(self)
        frm_botoes.pack(fill='x', padx=10, pady=10)

        tk.Button(frm_botoes, text="Novo Piloto", command=self.abrir_formulario).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Editar", command=self.editar_selecionado).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Excluir", command=self.excluir_selecionado).pack(side='left', padx=5)

        # Tabela
        cols = ('id', 'nome', 'cpf', 'licensa', 'companhia')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('cpf', text='CPF')
        self.tree.heading('licensa', text='Licença')
        self.tree.heading('companhia', text='Companhia')

        self.tree.column('id', width=30)
        self.tree.column('nome', width=150)
        self.tree.column('cpf', width=100)
        self.tree.column('licensa', width=100)
        self.tree.column('companhia', width=150)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        # Mapear ID da companhia para o Nome para exibir na tabela
        companhias = {c.id: c.nome for c in self.controlador.get_all_companhias()}
        
        for p in self.controlador.get_all_pilotos():
            nome_comp = companhias.get(p.companhia_id, "Desconhecida")
            self.tree.insert('', 'end', values=(p.id, p.nome, p.cpf, p.codigoDeLicensa, nome_comp))

    def _get_id_selecionado(self):
        sel = self.tree.focus()
        if not sel: return None
        try:
            valor = self.tree.item(sel)['values'][0]
            return int(valor)
        except (ValueError, IndexError):
            return None

    def excluir_selecionado(self):
        id_piloto = self._get_id_selecionado()
        if id_piloto is None: return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir este piloto?"):
            sucesso, msg = self.controlador.excluir(id_piloto)
            if sucesso:
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def abrir_formulario(self, piloto=None):
        FormularioPiloto(self, self.controlador, self.atualizar_lista, piloto)

    def editar_selecionado(self):
        id_piloto = self._get_id_selecionado()
        if id_piloto is None: return
        
        # Recupera o objeto do banco
        piloto = self.controlador.piloto_dao.get_by_id(id_piloto)
        if piloto:
            self.abrir_formulario(piloto)
        else:
            messagebox.showerror("Erro", "Piloto não encontrado.")


class FormularioPiloto(tk.Toplevel):
    def __init__(self, parent, controlador, callback, piloto=None):
        super().__init__(parent)
        self.controlador = controlador
        self.callback = callback
        self.piloto = piloto
        
        self.title("Cadastro de Piloto" if not piloto else "Editar Piloto")
        self.geometry("400x400")
        
        # Carrega dados para o Combobox
        self.comps = self.controlador.get_all_companhias()
        self.map_nome_id = {c.nome: c.id for c in self.comps}
        self.map_id_nome = {c.id: c.nome for c in self.comps}
        
        self._criar_campos()
        if piloto: self._preencher()

    def _criar_campos(self):
        self.entries = {}
        frm = tk.Frame(self)
        frm.pack(padx=10, pady=10, fill='both', expand=True)

        tk.Label(frm, text="Companhia Aérea:").pack(anchor='w')
        self.combo_comp = ttk.Combobox(frm, values=list(self.map_nome_id.keys()), state="readonly")
        self.combo_comp.pack(fill='x', pady=(0, 5))

        def add_field(label, key):
            tk.Label(frm, text=label).pack(anchor='w')
            e = tk.Entry(frm)
            e.pack(fill='x', pady=(0, 5))
            self.entries[key] = e

        add_field("Nome Completo:", "nome")
        add_field("CPF:", "cpf")
        add_field("Código da Licença:", "codigoDeLicensa")

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=20)

    def _preencher(self):
        p = self.piloto
        if p is None: return

        self.entries['nome'].insert(0, p.nome)
        self.entries['cpf'].insert(0, p.cpf)
        self.entries['codigoDeLicensa'].insert(0, p.codigoDeLicensa)
        
        nome_comp = self.map_id_nome.get(p.companhia_id)
        if nome_comp:
            self.combo_comp.set(nome_comp)

    def salvar(self):
        nome_comp = self.combo_comp.get()
        comp_id = self.map_nome_id.get(nome_comp)
        
        dados = {
            'nome': self.entries['nome'].get(),
            'cpf': self.entries['cpf'].get(),
            'codigoDeLicensa': self.entries['codigoDeLicensa'].get(),
            'companhia_id': comp_id
        }

        if self.piloto:
            sucesso, msg = self.controlador.atualizar(self.piloto.id, dados)
        else:
            sucesso, msg = self.controlador.cadastrar(dados)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", msg)