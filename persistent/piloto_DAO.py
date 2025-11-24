from .base_DAO import PickleDAO
from model.piloto import Piloto


class PilotoDAO(PickleDAO[Piloto]):
    def __init__(self):
        super().__init__('db_pilotos.pkl')

    def existem_pilotos_por_companhia(self, companhia_id: int) -> bool:
        for piloto in self.get_all():
            if piloto.companhia_id == companhia_id:
                return True
        return False