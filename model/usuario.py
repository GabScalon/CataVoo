from abc import ABC

class Usuario(ABC):
    
    def __init__(self, cpf, nome, email, login, senha_hash, salt, primeiro_acesso=True):
        self.__cpf = cpf 
        self.__nome = nome
        self.__email = email
        self.__login = login
        
        # Dados de Segurança (Nunca armazena a senha real)
        self.__senha_hash = senha_hash
        self.__salt = salt
        self.__primeiro_acesso = primeiro_acesso

    @property
    def cpf(self): return self.__cpf

    @property
    def nome(self): return self.__nome
    
    @nome.setter
    def nome(self, nome): self.__nome = nome
        
    @property
    def email(self): return self.__email
    
    @email.setter
    def email(self, email): self.__email = email

    @property
    def login(self): return self.__login

    @property
    def senha_hash(self): return self.__senha_hash
    
    @property
    def salt(self): return self.__salt

    @property
    def primeiro_acesso(self): return self.__primeiro_acesso

    def confirmar_primeiro_acesso(self):
        self.__primeiro_acesso = False

    def atualizar_senha(self, novo_hash, novo_salt):
        self.__senha_hash = novo_hash
        self.__salt = novo_salt

    def __repr__(self):
        return f"{self.__class__.__name__}(login='{self.login}')"

