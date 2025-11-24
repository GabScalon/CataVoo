import tkinter as tk
from tkinter import ttk, messagebox
from model.dto import CadastroUsuarioDTO, AlteracaoUsuarioDTO

class AdministradorView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.__controller = controller
        self.__cpf_em_memoria = None
        
        self.title("Gerenciar Usuários (Admin)")
        self.geometry("500x550")
        
        # Faz a janela ficar "presa" na frente da principal
        self.transient(parent)
        
        self.__setup_widgets()

    def __setup_widgets(self):
        # --- Frame de Busca ---
        frame_busca = ttk.Frame(self, padding=10)
        frame_busca.pack(fill='x')
        
        ttk.Label(frame_busca, text="CPF:").pack(side='left', padx=5)
        self.entry_cpf = ttk.Entry(frame_busca, width=20)
        self.entry_cpf.pack(side='left', padx=5, fill='x', expand=True)
        self.btn_checar = ttk.Button(frame_busca, text="Verificar CPF", command=self.__on_checar_cpf)
        self.btn_checar.pack(side='left', padx=5)

        # --- Frame do Formulário ---
        self.form_frame = ttk.LabelFrame(self, text="Dados do Usuário", padding=10)
        self.form_frame.pack(fill='x', padx=10, pady=10)
        
        # 1. Nome
        ttk.Label(self.form_frame, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_nome = ttk.Entry(self.form_frame, width=40)
        self.entry_nome.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # 2. Email
        ttk.Label(self.form_frame, text="Email:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_email = ttk.Entry(self.form_frame, width=40)
        self.entry_email.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # 3. Login (NOVO CAMPO)
        ttk.Label(self.form_frame, text="Login:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.entry_login = ttk.Entry(self.form_frame, width=20)
        self.entry_login.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # 4. Tipo de Usuário
        ttk.Label(self.form_frame, text="Tipo:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.tipo_usuario_var = tk.StringVar(self)
        self.option_tipo = ttk.OptionMenu(self.form_frame, self.tipo_usuario_var, "", "FUNCIONARIO", "ADMINISTRADOR")
        self.option_tipo.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        
        self.form_frame.columnconfigure(1, weight=1)

        # 5. Aviso de Senha (NOVO)
        lbl_aviso = tk.Label(self.form_frame, text="ℹ A senha inicial será os números do CPF.", fg="blue", font=("Arial", 8))
        lbl_aviso.grid(row=4, column=0, columnspan=2, pady=5)
        
        # --- Frame de Ações (Botões) ---
        frame_acoes = ttk.Frame(self, padding=10)
        frame_acoes.pack(fill='x')
        
        self.btn_incluir = ttk.Button(frame_acoes, text="Incluir", command=self.__on_incluir)
        self.btn_alterar = ttk.Button(frame_acoes, text="Salvar Alterações", command=self.__on_salvar_alteracoes)
        self.btn_excluir = ttk.Button(frame_acoes, text="Excluir", command=self.__on_excluir)
        
        self.btn_incluir.pack(side='left', padx=5, expand=True, fill='x')
        self.btn_alterar.pack(side='left', padx=5, expand=True, fill='x')
        self.btn_excluir.pack(side='left', padx=5, expand=True, fill='x')

        self.__habilitar_formulario(False)

    def __habilitar_formulario(self, habilitar_campos: bool, modo: str = "nenhum"):
        estado_campos = 'normal' if habilitar_campos else 'disabled'
        self.entry_nome.configure(state=estado_campos)
        self.entry_email.configure(state=estado_campos)
        
        # Login só pode ser editado na inclusão (não mudamos login depois de criado aqui)
        if modo == "incluir":
            self.entry_login.configure(state='normal')
            self.option_tipo.configure(state='normal')
        else:
            self.entry_login.configure(state='disabled')
            self.option_tipo.configure(state='disabled')

        self.btn_incluir.configure(state='normal' if modo == "incluir" else 'disabled')
        self.btn_alterar.configure(state='normal' if modo == "encontrado" else 'disabled')
        self.btn_excluir.configure(state='normal' if modo == "encontrado" else 'disabled')

    def __limpar_formulario(self):
        self.entry_nome.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_login.delete(0, 'end')
        self.tipo_usuario_var.set("FUNCIONARIO")

    def __preencher_formulario(self, usuario):
        self.entry_nome.insert(0, usuario.nome)
        self.entry_email.insert(0, usuario.email)
        self.entry_login.insert(0, usuario.login) # Preenche o login
        tipo = "ADMINISTRADOR" if "Administrador" in str(type(usuario)) else "FUNCIONARIO"
        self.tipo_usuario_var.set(tipo)

    def __on_checar_cpf(self):
        cpf = self.entry_cpf.get()
        status, data = self.__controller.checar_status_cpf(cpf)
        
        self.__limpar_formulario()
        
        if status == "ERRO":
            self.__habilitar_formulario(False)
            messagebox.showerror("Erro", data)
        
        elif status == "ENCONTRADO":
            usuario = data
            self.__cpf_em_memoria = usuario.cpf
            self.__habilitar_formulario(True, modo="encontrado")
            self.__preencher_formulario(usuario)
            
        elif status == "NAO_ENCONTRADO":
            cpf_validado = data
            self.__cpf_em_memoria = cpf_validado
            self.__habilitar_formulario(True, modo="incluir")
            messagebox.showinfo("Novo Cadastro", "CPF livre. Preencha os dados.")

    def __on_incluir(self):
        # --- CORREÇÃO: Validação para garantir que o CPF não é None ---
        if not self.__cpf_em_memoria:
            messagebox.showwarning("Aviso", "Por favor, verifique o CPF antes de incluir.")
            return

        # Aqui usamos o DTO atualizado sem a senha
        dto = CadastroUsuarioDTO(
            cpf=self.__cpf_em_memoria,
            nome=self.entry_nome.get(),
            email=self.entry_email.get(),
            login=self.entry_login.get(), 
            tipo_usuario=self.tipo_usuario_var.get()
        )
        
        status, msg = self.__controller.cadastrar_usuario(dto)

        if status == "SUCESSO":
            messagebox.showinfo("Sucesso", msg)
            self.__limpar_formulario()
            self.entry_cpf.delete(0, 'end')
            self.__habilitar_formulario(False)
            self.__cpf_em_memoria = None
        else:
            messagebox.showerror("Erro", msg)

    def __on_salvar_alteracoes(self):
        dto = AlteracaoUsuarioDTO(
            nome=self.entry_nome.get(),
            email=self.entry_email.get()
        )
        status, msg = self.__controller.alterar_usuario(self.__cpf_em_memoria, dto)
        
        if status == "SUCESSO":
            messagebox.showinfo("Sucesso", msg)
            self.__limpar_formulario()
            self.entry_cpf.delete(0, 'end')
            self.__habilitar_formulario(False)
        else:
            messagebox.showerror("Erro", msg)

    def __on_excluir(self):
        if messagebox.askyesno("Confirmar", f"Excluir usuário CPF {self.__cpf_em_memoria}?"):
            status, msg = self.__controller.excluir_usuario(self.__cpf_em_memoria)
            
            if status == "SUCESSO":
                messagebox.showinfo("Sucesso", msg)
                self.__limpar_formulario()
                self.entry_cpf.delete(0, 'end')
                self.__habilitar_formulario(False)
            else:
                messagebox.showerror("Erro", msg)