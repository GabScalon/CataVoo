class Aeronave:
    def __init__(self, modelo: str, lotacao_maxima: int):
        self.modelo = modelo
        self.lotacao_maxima = lotacao_maxima

    def __repr__(self):
        return f"Aeronave(modelo='{self.modelo}', lotacao_maxima={self.lotacao_maxima})"

