from typing import Optional, List
from endereco import Endereco


class Aeroporto:
    def __init__(self, nome: str, endereco: Endereco, ehPublico: bool = True, 
                 portoes: Optional[List[str]] = None, id: Optional[int] = None):
        self.nome = nome
        self.endereco = endereco
        self.ehPublico = ehPublico
        self.portoes = portoes if portoes is not None else []
        self.id = id