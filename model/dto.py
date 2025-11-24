from dataclasses import dataclass

@dataclass
class CadastroUsuarioDTO:
    cpf: str
    nome: str
    email: str
    login: str
    # Senha removida daqui (gerada automaticamente pelo sistema)
    tipo_usuario: str 

@dataclass
class AlteracaoUsuarioDTO:
    nome: str
    email: str