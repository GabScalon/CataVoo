from typing import Optional
from endereco import Endereco

class CompanhiaAerea:
    def __init__(self, nome: str, enderecoSede: Optional[Endereco] = None, 
                 numeroContato: str = "", email: str = "", 
                 id: Optional[int] = None):
        self.nome = nome
        self.enderecoSede = enderecoSede
        self.numeroContato = numeroContato
        self.email = email
        self.id = id

    @staticmethod
    def create(dadosCompanhia: dict):
        return CompanhiaAerea(**dadosCompanhia)

    def setEndereco(self, endereco: Endereco):
        self.enderecoSede = endereco