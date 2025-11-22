from typing import Optional


class Usuario:
    def __init__(self, nome: str, login: str, senha: str, 
                 codigoID: Optional[int] = None):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.codigoID = codigoID if codigoID is not None else (hash(login) % 100000)