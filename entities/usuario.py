from typing import Optional


class Usuario:
    def __init__(self, nome: str, login: str, senha: str, 
                 id: Optional[int] = None):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.id = id