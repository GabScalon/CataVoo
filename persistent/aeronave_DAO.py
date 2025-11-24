from .base_DAO import PickleDAO
from model.aeronave import Aeronave

class AeronaveDAO(PickleDAO[Aeronave]):
    def __init__(self):
        super().__init__('db_aeronaves.pkl')
    
    # Método auxiliar
    def get_capacidade(self, aeronave_id: int) -> int:
        aeronave = self.get_by_id(aeronave_id)
        if aeronave:
            return aeronave.lotacaoMaxima
        return 0

    def existem_aeronaves_por_companhia(self, companhia_id: int) -> bool:
        for aeronave in self.get_all():
            if aeronave.companhia_id == companhia_id:
                return True
        return False