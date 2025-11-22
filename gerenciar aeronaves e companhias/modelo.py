from typing import List, Optional
from datetime import datetime
from enum import Enum

class Endereco:
    def __init__(self, rua: str, cidade: str, estado: str, pais: str, 
                 numero: int = 0, bairro: str = "", complemento: str = "", 
                 id: Optional[int] = None):
        self.rua = rua
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        self.numero = numero
        self.bairro = bairro
        self.complemento = complemento
        self.id = id

    @staticmethod
    def create(dadosEndereco: dict):
        return Endereco(**dadosEndereco)

class CompanhiaAerea:
    def __init__(self, nome: str, enderecoSede: Optional[Endereco] = None, 
                 numeroContato: str = "", email: str = "", 
                 id: Optional[int] = None):
        self.nome = nome
        self.enderecoSede = enderecoSede
        self.numeroContato = numeroContato
        self.email = email
        self.id = id

    @staticmethod
    def create(dadosCompanhia: dict):
        return CompanhiaAerea(**dadosCompanhia)

    def setEndereco(self, endereco: Endereco):
        self.enderecoSede = endereco

class Aeronave:
    def __init__(self, modelo: str, companhia_id: int, capacidadeDeCarga: float,
                 lotacaoMaxima: int, tipoDeAviao: str = "", 
                 id: Optional[int] = None):
        self.modelo = modelo
        self.companhia_id = companhia_id
        self.capacidadeDeCarga = capacidadeDeCarga
        self.lotacaoMaxima = lotacaoMaxima
        self.tipoDeAviao = tipoDeAviao
        self.id = id
    
    @staticmethod
    def create(dadosAeronave: dict):
        return Aeronave(**dadosAeronave)

class Piloto:
    def __init__(self, nome: str, companhia_id: int, cpf: str = "",
                 codigoDeLicensa: str = "", id: Optional[int] = None):
        self.nome = nome
        self.companhia_id = companhia_id
        self.cpf = cpf
        self.codigoDeLicensa = codigoDeLicensa
        self.id = id

class Aeroporto:
    def __init__(self, nome: str, endereco: Endereco, ehPublico: bool = True, 
                 portoes: Optional[List[str]] = None, id: Optional[int] = None):
        self.nome = nome
        self.endereco = endereco
        self.ehPublico = ehPublico
        self.portoes = portoes if portoes is not None else []
        self.id = id

class TipoDeVoo(Enum):
    COMERCIAL = 1
    CARGA = 2
    PARTICULAR = 3

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

class Usuario:
    def __init__(self, nome: str, login: str, senha: str, 
                 codigoID: Optional[int] = None):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.codigoID = codigoID if codigoID is not None else (hash(login) % 100000)

class Administrador(Usuario):
    def __init__(self, nome: str, login: str, senha: str, 
                 aeroporto_id: int, cpf: str,
                 codigoID: Optional[int] = None):
        super().__init__(nome, login, senha, codigoID)
        self.aeroporto_id = aeroporto_id
        self.cpf = cpf