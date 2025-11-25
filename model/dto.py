from dataclasses import dataclass

@dataclass
class CadastroUsuarioDTO:
    cpf: str
    nome: str
    email: str
    login: str
    tipo_usuario: str 

@dataclass
class AlteracaoUsuarioDTO:
    nome: str
    email: str