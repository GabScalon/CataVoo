import tkinter as tk
from tkinter import ttk, messagebox
from controllers.aeronave_controller import AeronaveController

class ViewAeronave(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciar Aeronaves")
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()

        self.controlador = AeronaveController()
        
        self._criar_widgets()
        self.atualizar_lista()

    def _criar_widgets(self):
        frm_botoes = tk.Frame(self)
        frm_botoes.pack(fill='x', padx=10, pady=10)

        tk.Button(frm_botoes, text="Nova Aeronave", command=self.abrir_formulario).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Editar", command=self.editar_selecionado).pack(side='left', padx=5)
        tk.Button(frm_botoes, text="Excluir", command=self.excluir_selecionado).pack(side='left', padx=5)

        cols = ('id', 'modelo', 'companhia', 'capacidade')
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('modelo', text='Modelo')
        self.tree.heading('companhia', text='Companhia')
        self.tree.heading('capacidade', text='Capacidade (Pax)')

        self.tree.column('id', width=30)
        self.tree.column('modelo', width=150)
        self.tree.column('companhia', width=150)
        self.tree.column('capacidade', width=100)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        companhias = {c.id: c.nome for c in self.controlador.get_all_companhias()}
        
        for aero in self.controlador.get_all_aeronaves():
            nome_comp = companhias.get(aero.companhia_id, "Desconhecida")
            self.tree.insert('', 'end', values=(aero.id, aero.modelo, nome_comp, aero.lotacaoMaxima))

    def _get_id_selecionado(self):
        sel = self.tree.focus()
        if not sel: return None
        try:
            valor = self.tree.item(sel)['values'][0]
            return int(valor)
        except (ValueError, IndexError):
            return None

    def excluir_selecionado(self):
        id_aero = self._get_id_selecionado()
        if id_aero is None: return
        
        if messagebox.askyesno("Confirmar", "Deseja excluir esta aeronave?"):
            sucesso, msg = self.controlador.excluir(id_aero)
            if sucesso:
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def abrir_formulario(self, aeronave=None):
        FormularioAeronave(self, self.controlador, self.atualizar_lista, aeronave)

    def editar_selecionado(self):
        id_aero = self._get_id_selecionado()
        if id_aero is None: return
        
        aero = self.controlador.aeronave_dao.get_by_id(id_aero)
        if aero:
            self.abrir_formulario(aero)
        else:
            messagebox.showerror("Erro", "Aeronave não encontrada.")


class FormularioAeronave(tk.Toplevel):
    def __init__(self, parent, controlador, callback, aeronave=None):
        super().__init__(parent)
        self.controlador = controlador
        self.callback = callback
        self.aeronave = aeronave
        
        self.title("Aeronave")
        self.geometry("400x350")
        
        self.comps = self.controlador.get_all_companhias()
        self.map_nome_id = {c.nome: c.id for c in self.comps}
        self.map_id_nome = {c.id: c.nome for c in self.comps}
        
        self._criar_campos()
        if aeronave: self._preencher()

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

        add_field("Modelo:", "modelo")
        add_field("Tipo de Avião:", "tipoDeAviao")
        add_field("Lotação Máxima:", "lotacaoMaxima")
        add_field("Capacidade Carga (kg):", "capacidadeDeCarga")

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=10)

    def _preencher(self):
        a = self.aeronave
        
        # --- CORREÇÃO APLICADA: Cláusula de Guarda ---
        if a is None:
            return

        self.entries['modelo'].insert(0, a.modelo)
        self.entries['tipoDeAviao'].insert(0, a.tipoDeAviao)
        # Converter numeros para string ao inserir
        self.entries['lotacaoMaxima'].insert(0, str(a.lotacaoMaxima))
        self.entries['capacidadeDeCarga'].insert(0, str(a.capacidadeDeCarga))
        
        nome = self.map_id_nome.get(a.companhia_id)
        if nome: self.combo_comp.set(nome)

    def salvar(self):
        nome_comp = self.combo_comp.get()
        comp_id = self.map_nome_id.get(nome_comp)
        
        dados = {
            'modelo': self.entries['modelo'].get(),
            'companhia_id': comp_id,
            'tipoDeAviao': self.entries['tipoDeAviao'].get(),
            'lotacaoMaxima': self.entries['lotacaoMaxima'].get(),
            'capacidadeDeCarga': self.entries['capacidadeDeCarga'].get()
        }

        if self.aeronave:
            sucesso, msg = self.controlador.atualizar(self.aeronave.id, dados)
        else:
            sucesso, msg = self.controlador.cadastrar(dados)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Erro", msg)