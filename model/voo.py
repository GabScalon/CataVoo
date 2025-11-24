from typing import Optional
from datetime import datetime
from .tipo_de_voo import TipoDeVoo


class Voo:
    def __init__(self, 
                 codigo: str, 
                 aeronave_id: int, 
                 companhia_id: int, 
                 piloto_id: int, 
                 localDeSaida_id: int, 
                 destino_id: int, 
                 horarioDePartidaPrevisto: datetime, 
                 horarioDeChegadaPrevisto: datetime, 
                 statusDoVoo: str = "Agendado", 
                 tipoDeVoo: TipoDeVoo = TipoDeVoo.COMERCIAL,
                 numeroDePassageiros: int = 0,
                 carga: float = 0.0,
                 distanciaDeVoo: float = 0.0,
                 portao: str = "",
                 horarioRealDePartida: Optional[datetime] = None,
                 horarioRealDeChegada: Optional[datetime] = None,
                 id: Optional[int] = None):
        
        self.codigo = codigo
        self.aeronave_id = aeronave_id
        self.companhia_id = companhia_id
        self.piloto_id = piloto_id
        self.localDeSaida_id = localDeSaida_id
        self.destino_id = destino_id
        self.horarioDePartidaPrevisto = horarioDePartidaPrevisto
        self.horarioDeChegadaPrevisto = horarioDeChegadaPrevisto
        self.horarioRealDePartida = horarioRealDePartida
        self.horarioRealDeChegada = horarioRealDeChegada
        self.statusDoVoo = statusDoVoo
        self.tipoDeVoo = tipoDeVoo
        self.numeroDePassageiros = numeroDePassageiros
        self.carga = carga
        self.distanciaDeVoo = distanciaDeVoo
        self.portao = portao
        self.id = id