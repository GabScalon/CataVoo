import tkinter as tk
from tkinter import ttk, messagebox
from controllers.aeroporto_controller import AeroportoController

class ViewAeroporto(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Aeroportos")
        self.geometry("800x500")
        self.transient(parent)
        self.grab_set()

        self.controlador = AeroportoController()
        self._criar_widgets()
        self.atualizar_lista()

    def _criar_widgets(self):
        # Botões
        frm_botoes = tk.Frame(self)
        frm_botoes.pack(fill='x', padx=10, pady=10)

        tk.Button(frm_botoes, text="Novo Aeroporto", command=self.abrir_formulario).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Editar", command=self.editar_selecionado).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Excluir", command=self.excluir_selecionado).pack(side='left', padx=5)

        # Tabela
        cols = ('id', 'nome', 'cidade', 'estado', 'tipo', 'portoes')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('cidade', text='Cidade')
        self.tree.heading('estado', text='UF')
        self.tree.heading('tipo', text='Tipo')
        self.tree.heading('portoes', text='Portões')

        self.tree.column('id', width=30)
        self.tree.column('nome', width=200)
        self.tree.column('cidade', width=100)
        self.tree.column('estado', width=40)
        self.tree.column('tipo', width=60)
        self.tree.column('portoes', width=150)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for a in self.controlador.get_all_aeroportos():
            tipo = "Público" if a.ehPublico else "Privado"
            portoes_str = ", ".join(a.portoes) if a.portoes else "-"
            
            self.tree.insert('', 'end', values=(
                a.id, a.nome, a.endereco.cidade, a.endereco.estado, tipo, portoes_str
            ))

    def _get_id_selecionado(self):
        sel = self.tree.focus()
        if not sel: return None
        try:
            return int(self.tree.item(sel)['values'][0])
        except: return None

    def excluir_selecionado(self):
        id_aero = self._get_id_selecionado()
        if not id_aero: return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir este aeroporto?"):
            sucesso, msg = self.controlador.excluir(id_aero)
            if sucesso:
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def abrir_formulario(self, aeroporto=None):
        FormularioAeroporto(self, self.controlador, self.atualizar_lista, aeroporto)

    def editar_selecionado(self):
        id_aero = self._get_id_selecionado()
        if not id_aero: return
        
        aero = self.controlador.aeroporto_dao.get_by_id(id_aero)
        if aero:
            self.abrir_formulario(aero)
        else:
            messagebox.showerror("Erro", "Aeroporto não encontrado.")


class FormularioAeroporto(tk.Toplevel):
    def __init__(self, parent, controlador, callback, aeroporto=None):
        super().__init__(parent)
        self.controlador = controlador
        self.callback = callback
        self.aeroporto = aeroporto
        
        self.title("Cadastro de Aeroporto")
        self.geometry("500x500")
        
        self._criar_campos()
        if aeroporto: self._preencher()

    def _criar_campos(self):
        self.entries = {}
        
        # --- Frame Principal ---
        frm = tk.Frame(self, padx=10, pady=10)
        frm.pack(fill='both', expand=True)

        # Helper para criar Label + Entry
        def add_field(label, key, parent_frame=frm):
            tk.Label(parent_frame, text=label).pack(anchor='w')
            e = tk.Entry(parent_frame)
            e.pack(fill='x', pady=(0, 5))
            self.entries[key] = e

        # Dados Gerais
        tk.Label(frm, text="Dados do Aeroporto", font=('bold')).pack(anchor='w', pady=5)
        add_field("Nome:", "nome")
        
        # Checkbox Tipo
        self.var_publico = tk.BooleanVar(value=True)
        tk.Checkbutton(frm, text="Aeroporto Público", variable=self.var_publico).pack(anchor='w', pady=5)
        
        add_field("Portões (separe por vírgula, ex: A1, B2):", "portoes_str")

        # Endereço
        tk.Label(frm, text="Localização", font=('bold')).pack(anchor='w', pady=(15, 5))
        
        # Grid para endereço ficar mais organizado
        frm_end = tk.Frame(frm)
        frm_end.pack(fill='x')
        
        # Coluna 1
        f1 = tk.Frame(frm_end); f1.pack(side='left', fill='x', expand=True, padx=(0,5))
        add_field("Rua:", "rua", f1)
        add_field("Bairro:", "bairro", f1)
        add_field("Estado (UF):", "estado", f1)

        # Coluna 2
        f2 = tk.Frame(frm_end); f2.pack(side='left', fill='x', expand=True, padx=(5,0))
        add_field("Número:", "numero", f2)
        add_field("Cidade:", "cidade", f2)
        add_field("País:", "pais", f2)

        tk.Button(self, text="Salvar", command=self.salvar, height=2, bg="#ddffdd").pack(fill='x', padx=20, pady=20)

    def _preencher(self):
        a = self.aeroporto
        if not a: return

        self.entries['nome'].insert(0, a.nome)
        self.var_publico.set(a.ehPublico)
        
        # Converte lista de portões para string
        portoes_str = ", ".join(a.portoes)
        self.entries['portoes_str'].insert(0, portoes_str)

        if a.endereco:
            e = a.endereco
            self.entries['rua'].insert(0, e.rua)
            self.entries['numero'].insert(0, str(e.numero))
            self.entries['bairro'].insert(0, e.bairro)
            self.entries['cidade'].insert(0, e.cidade)
            self.entries['estado'].insert(0, e.estado)
            self.entries['pais'].insert(0, e.pais)

    def salvar(self):
        # Coleta dados do Aeroporto
        dados_aero = {
            'nome': self.entries['nome'].get(),
            'ehPublico': self.var_publico.get(),
            'portoes_str': self.entries['portoes_str'].get()
        }
        
        # Coleta dados do Endereço
        dados_end = {k: self.entries[k].get() for k in ['rua', 'numero', 'bairro', 'cidade', 'estado', 'pais']}

        if self.aeroporto:
            sucesso, msg = self.controlador.atualizar(self.aeroporto.id, dados_aero, dados_end)
        else:
            sucesso, msg = self.controlador.cadastrar(dados_aero, dados_end)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", msg)