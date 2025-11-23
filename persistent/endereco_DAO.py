from .base_DAO import PickleDAO
from entities.endereco import Endereco


class EnderecoDAO(PickleDAO[Endereco]):
    def __init__(self):
        super().__init__('db_enderecos.pkl')