import pickle
from models.voo import Voo

class VooDAO:
    ARQUIVO = "voos.pkl"

    @staticmethod
    def carregar():
        try:
            with open(VooDAO.ARQUIVO, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    @staticmethod
    def salvar(voos):
        with open(VooDAO.ARQUIVO, "wb") as f:
            pickle.dump(voos, f)

