from .base_DAO import PickleDAO
from model.endereco import Endereco


class EnderecoDAO(PickleDAO[Endereco]):
    def __init__(self):
        super().__init__('db_enderecos.pkl')