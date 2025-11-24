from .base_DAO import PickleDAO
from model.aeroporto import Aeroporto


class AeroportoDAO(PickleDAO[Aeroporto]):
    def __init__(self):
        super().__init__('db_aeroportos.pkl')