from .administrador import Administrador
from .aeronave import Aeronave
from .aeroporto import Aeroporto
from .companhia_aerea import CompanhiaAerea
from .endereco import Endereco
from .piloto import Piloto
from .tipo_de_voo import TipoDeVoo
from .usuario import Usuario
from .voo import Voo


"""
Permite importar tudo numa linha, por exemplo, 'from entities import CompanhiaAerea, Endereco, Aeronave'
ao invés de, por exemplo,
'from entities.companhia_aerea import CompanhiaAerea
from entities.endereco import Endereco
from entities.aeronave import Aeronave'
"""
