from .base_DAO import PickleDAO
from model.voo import Voo

# [Voo] representa que o T em "Generic[T]" é Voo
class VooDAO(PickleDAO[Voo]):
    def __init__(self):
        super().__init__('db_voos.pkl')

    def existem_voos_para_aeronave(self, aeronave_id: int) -> bool:
            """Verifica se existe algum voo agendado para uma aeronave específica."""
            for voo in self.get_all():
                if voo.aeronave_id == aeronave_id:
                    return True
            return False

    def buscar_por_codigo(self, codigo: str) -> list[Voo]:
        return [v for v in self.get_all() if codigo.lower() in v.codigo.lower()]

    def buscar_por_destino(self, aeroporto_id: int) -> list[Voo]:
        return [v for v in self.get_all() if v.destino_id == aeroporto_id]