import tkinter as tk
from tkinter import ttk, messagebox
from services.cadastro_service import CadastroService
import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Voos ✈️")
        self.geometry("700x450")
        self.service = CadastroService()

        # Campos
        tk.Label(self, text="Código do Voo:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_entry = tk.Entry(self)
        self.codigo_entry.grid(row=0, column=1)

        tk.Label(self, text="Partida (YYYY-MM-DD HH:MM):").grid(row=1, column=0)
        self.partida_entry = tk.Entry(self)
        self.partida_entry.grid(row=1, column=1)

        tk.Label(self, text="Chegada (YYYY-MM-DD HH:MM):").grid(row=2, column=0)
        self.chegada_entry = tk.Entry(self)
        self.chegada_entry.grid(row=2, column=1)

        tk.Label(self, text="Aeronave:").grid(row=3, column=0)
        self.aeronave_combo = ttk.Combobox(self, values=self.service.listar_aeronaves_modelos())
        self.aeronave_combo.grid(row=3, column=1)

        tk.Label(self, text="Nº Passageiros:").grid(row=4, column=0)
        self.passageiros_entry = tk.Entry(self)
        self.passageiros_entry.grid(row=4, column=1)

        tk.Button(self, text="Cadastrar Voo", command=self.cadastrar_voo).grid(row=5, column=1, pady=10)

        # Lista de voos
        self.tree = ttk.Treeview(self, columns=("codigo", "partida", "chegada", "aeronave", "passageiros"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        tk.Button(self, text="Atualizar Lista", command=self.atualizar_lista_voos).grid(row=7, column=1)

    def cadastrar_voo(self):
        try:
            codigo = self.codigo_entry.get()
            partida = datetime.datetime.strptime(self.partida_entry.get(), "%Y-%m-%d %H:%M")
            chegada = datetime.datetime.strptime(self.chegada_entry.get(), "%Y-%m-%d %H:%M")
            modelo = self.aeronave_combo.get()
            passageiros = int(self.passageiros_entry.get())

            self.service.cadastrar_voo("func1", codigo, partida, chegada, modelo, passageiros)
            messagebox.showinfo("Sucesso", f"Voo {codigo} cadastrado com sucesso!")
            self.atualizar_lista_voos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def atualizar_lista_voos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for voo in self.service.listar_voos():
            self.tree.insert("", "end", values=(voo.codigo, voo.horario_partida, voo.horario_chegada,
                                                voo.aeronave.modelo, voo.numero_passageiros))

