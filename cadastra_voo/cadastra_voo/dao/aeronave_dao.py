import pickle
from models.aeronave import Aeronave

class AeronaveDAO:
    ARQUIVO = "aeronaves.pkl"

    @staticmethod
    def carregar():
        try:
            with open(AeronaveDAO.ARQUIVO, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    @staticmethod
    def salvar(aeronaves):
        with open(AeronaveDAO.ARQUIVO, "wb") as f:
            pickle.dump(aeronaves, f)

