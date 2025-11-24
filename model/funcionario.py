from model import Usuario

class Funcionario(Usuario):
    def __init__(self, cpf, nome, email, login, senha_hash, salt, primeiro_acesso=True):
        super().__init__(cpf, nome, email, login, senha_hash, salt, primeiro_acesso)
