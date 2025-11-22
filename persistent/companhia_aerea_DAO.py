from .base_DAO import PickleDAO
from entities.companhia_aerea import CompanhiaAerea

# [CompanhiaAerea] representa que o T em "Generic[T]" é CompanhiaAerea
class CompanhiaAereaDAO(PickleDAO[CompanhiaAerea]):
    def __init__(self):
        super().__init__('db_companhias_aereas.pkl')
