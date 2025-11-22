from typing import Optional
from entities.usuario import Usuario
from .base_DAO import PickleDAO


class UsuarioDAO(PickleDAO[Usuario]):
    def __init__(self):
        # Define o nome do arquivo onde todos os usuários (e admins) serão salvos
        super().__init__('db_usuarios.pkl')

    def get_by_login(self, login: str) -> Optional[Usuario]:
        """
        Busca um usuário pelo login. 
        Retorna o objeto Usuario (ou Administrador) se encontrar, ou None.
        """
        for usuario in self.get_all():
            if usuario.login == login:
                return usuario
        return None