from typing import Optional


class Aeronave:
    def __init__(self, modelo: str, companhia_id: int, capacidadeDeCarga: float,
                 lotacaoMaxima: int, tipoDeAviao: str = "", 
                 id: Optional[int] = None):
        self.modelo = modelo
        self.companhia_id = companhia_id
        self.capacidadeDeCarga = capacidadeDeCarga
        self.lotacaoMaxima = lotacaoMaxima
        self.tipoDeAviao = tipoDeAviao
        self.id = id
    
    @staticmethod
    def create(dadosAeronave: dict):
        return Aeronave(**dadosAeronave)