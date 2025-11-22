from typing import Optional
from usuario import Usuario


class Administrador(Usuario):
    def __init__(self, nome: str, login: str, senha: str, 
                 aeroporto_id: int, cpf: str,
                 codigoID: Optional[int] = None):
        super().__init__(nome, login, senha, codigoID)
        self.aeroporto_id = aeroporto_id
        self.cpf = cpf