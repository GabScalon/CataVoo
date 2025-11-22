from typing import Optional

class Endereco:
    def __init__(self, rua: str, cidade: str, estado: str, pais: str, 
                 numero: int = 0, bairro: str = "", complemento: str = "", 
                 id: Optional[int] = None):
        self.rua = rua
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.numero = numero
        self.bairro = bairro
        self.complemento = complemento
        self.id = id

    @staticmethod
    def create(dadosEndereco: dict):
        return Endereco(**dadosEndereco)