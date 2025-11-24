import datetime
from models.aeronave import Aeronave

class Voo:
    def __init__(self, codigo: str, horario_partida: datetime.datetime, horario_chegada: datetime.datetime,
                 aeronave: Aeronave, num_passageiros: int):
        self.codigo = codigo
        self.horario_partida = horario_partida
        self.horario_chegada = horario_chegada
        self.aeronave = aeronave
        self.numero_passageiros = num_passageiros
        self.status = "Programado"

    def __repr__(self):
        return (f"Voo(codigo='{self.codigo}', partida='{self.horario_partida}', "
                f"chegada='{self.horario_chegada}', aeronave='{self.aeronave.modelo}', "
                f"passageiros={self.numero_passageiros}, status='{self.status}')")

