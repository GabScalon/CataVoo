import datetime
from dao.aeronave_dao import AeronaveDAO
from dao.voo_dao import VooDAO
from models.aeronave import Aeronave
from models.voo import Voo
from models.usuario import Usuario

class CadastroService:
    def __init__(self):
        self.db_aeronaves = AeronaveDAO.carregar()
        self.db_voos = VooDAO.carregar()

        if not self.db_aeronaves:
            self.db_aeronaves["B737"] = Aeronave("Boeing 737", 162)
            self.db_aeronaves["A320"] = Aeronave("Airbus A320", 180)
            AeronaveDAO.salvar(self.db_aeronaves)

    def listar_aeronaves_modelos(self):
        return list(self.db_aeronaves.keys())

    def listar_aeronaves(self):
        return list(self.db_aeronaves.values())

    def listar_voos(self):
        return list(self.db_voos.values())

    def cadastrar_aeronave(self, modelo: str, lotacao_maxima: int):
        if modelo in self.db_aeronaves:
            raise ValueError(f"Aeronave '{modelo}' já cadastrada.")
        nova = Aeronave(modelo, lotacao_maxima)
        self.db_aeronaves[modelo] = nova
        AeronaveDAO.salvar(self.db_aeronaves)
        return nova

    def cadastrar_voo(self, usuario_login: str, codigo: str, horario_partida: datetime.datetime,
                      horario_chegada: datetime.datetime, modelo_aeronave: str, numero_passageiros: int):

        if codigo in self.db_voos:
            raise ValueError(f"O código de voo '{codigo}' já existe.")
        if horario_chegada <= horario_partida:
            raise ValueError("Horário de chegada deve ser posterior ao de partida.")
        aeronave = self.db_aeronaves.get(modelo_aeronave)
        if not aeronave:
            raise ValueError(f"Aeronave '{modelo_aeronave}' não encontrada.")
        if numero_passageiros > aeronave.lotacao_maxima:
            raise ValueError(f"Número de passageiros ({numero_passageiros}) excede a capacidade ({aeronave.lotacao_maxima}).")

        usuario = Usuario(usuario_login, "Funcionário", "funcionario")
        novo_voo = Voo(codigo, horario_partida, horario_chegada, aeronave, numero_passageiros)
        self.db_voos[codigo] = novo_voo
        VooDAO.salvar(self.db_voos)
        return novo_voo

