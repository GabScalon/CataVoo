from .usuario import Usuario

class Administrador(Usuario):
    def __init__(self, cpf, nome, email, login, senha_hash, salt, primeiro_acesso=True):
        super().__init__(cpf, nome, email, login, senha_hash, salt, primeiro_acesso)