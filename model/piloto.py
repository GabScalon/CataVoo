from typing import Optional


class Piloto:
    def __init__(self, nome: str, companhia_id: int, cpf: str = "",
                 codigoDeLicensa: str = "", id: Optional[int] = None):
        self.nome = nome
        self.companhia_id = companhia_id
        self.cpf = cpf
        self.codigoDeLicensa = codigoDeLicensa
        self.id = id