import tkinter as tk
from tkinter import ttk, messagebox
from controllers.companhia_controller import CompanhiaController

class ViewCompanhia(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Companhias Aéreas")
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()

        self.controlador = CompanhiaController()
        
        self._criar_widgets()
        self.atualizar_lista()

    def _criar_widgets(self):
        frm_botoes = tk.Frame(self)
        frm_botoes.pack(fill='x', padx=10, pady=10)

        tk.Button(frm_botoes, text="Nova Companhia", command=self.abrir_formulario).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Editar", command=self.editar_selecionado).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Excluir", command=self.excluir_selecionado).pack(side='left', padx=5)

        cols = ('id', 'nome', 'email', 'contato')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('email', text='Email')
        self.tree.heading('contato', text='Contato')

        self.tree.column('id', width=30)
        self.tree.column('nome', width=150)
        self.tree.column('email', width=150)
        self.tree.column('contato', width=100)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for comp in self.controlador.get_all_companhias():
            self.tree.insert('', 'end', values=(comp.id, comp.nome, comp.email, comp.numeroContato))

    def _get_id_selecionado(self):
        sel = self.tree.focus()
        if not sel: return None
        # CORREÇÃO AQUI: Convertendo explicitamente para int
        try:
            valor = self.tree.item(sel)['values'][0]
            return int(valor)
        except (ValueError, IndexError):
            return None

    def excluir_selecionado(self):
        id_comp = self._get_id_selecionado()
        if id_comp is None: return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir esta companhia?"):
            sucesso, msg = self.controlador.excluir(id_comp)
            if sucesso:
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def abrir_formulario(self, companhia=None):
        FormularioCompanhia(self, self.controlador, self.atualizar_lista, companhia)

    def editar_selecionado(self):
        id_comp = self._get_id_selecionado()
        if id_comp is None: return
        
        # Agora id_comp é garantidamente um int
        comp = self.controlador.companhia_dao.get_by_id(id_comp)
        if comp:
            self.abrir_formulario(comp)
        else:
            messagebox.showerror("Erro", "Companhia não encontrada.")


class FormularioCompanhia(tk.Toplevel):
    def __init__(self, parent, controlador, callback, companhia=None):
        super().__init__(parent)
        self.controlador = controlador
        self.callback = callback
        self.companhia = companhia
        
        self.title("Cadastro de Companhia" if not companhia else "Edição de Companhia")
        self.geometry("400x450")
        
        self._criar_campos()
        if companhia: self._preencher()

    def _criar_campos(self):
        self.entries = {}
        frm = tk.Frame(self)
        frm.pack(padx=10, pady=10, fill='both', expand=True)

        def add_field(label, key):
            tk.Label(frm, text=label).pack(anchor='w')
            e = tk.Entry(frm)
            e.pack(fill='x', pady=(0, 5))
            self.entries[key] = e

        tk.Label(frm, text="Dados Gerais", font=('bold')).pack(anchor='w', pady=5)
        add_field("Nome:", "nome")
        add_field("Email:", "email")
        add_field("Telefone:", "numeroContato")

        tk.Label(frm, text="Endereço da Sede", font=('bold')).pack(anchor='w', pady=10)
        add_field("Rua:", "rua")
        add_field("Número:", "numero")
        add_field("Bairro:", "bairro")
        add_field("Cidade:", "cidade")
        add_field("Estado:", "estado")
        add_field("País:", "pais")

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=10)

    def _preencher(self):
        c = self.companhia
        
        if c is None:
            return

        self.entries['nome'].insert(0, c.nome)
        self.entries['email'].insert(0, c.email)
        self.entries['numeroContato'].insert(0, c.numeroContato)
        
        if c.enderecoSede:
            e = c.enderecoSede
            self.entries['rua'].insert(0, e.rua)
            self.entries['numero'].insert(0, str(e.numero)) 
            self.entries['bairro'].insert(0, e.bairro)
            self.entries['cidade'].insert(0, e.cidade)
            self.entries['estado'].insert(0, e.estado)
            self.entries['pais'].insert(0, e.pais)

    def salvar(self):
        dados_comp = {k: self.entries[k].get() for k in ['nome', 'email', 'numeroContato']}
        dados_end = {k: self.entries[k].get() for k in ['rua', 'numero', 'bairro', 'cidade', 'estado', 'pais']}

        if self.companhia:
            sucesso, msg = self.controlador.atualizar(self.companhia.id, dados_comp, dados_end)
        else:
            sucesso, msg = self.controlador.cadastrar(dados_comp, dados_end)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", msg)