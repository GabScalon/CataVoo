from persistent import UsuarioDAO
from entities import Usuario, Administrador


class UsuarioController:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def autenticar(self, login: str, senha: str):
        usuario = self.usuario_dao.get_by_login(login)
        
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def buscar_todos(self):
        return self.usuario_dao.get_all()

    def cadastrar(self, dados: dict, eh_admin: bool = False):
        """
        Cria um novo usuário.
        :param dados: Dicionário com nome, login, senha e (se admin) cpf, aeroporto_id.
        :param eh_admin: Booleano definindo se cria Administrador ou Usuario comum.
        """
        login = dados.get('login')
        if not login:
             return False, "Erro: Login é obrigatório."
             
        if self.usuario_dao.get_by_login(login):
            return False, f"Erro: O login '{login}' já está em uso."

        try:
            if eh_admin:
                novo_usuario = Administrador(
                    nome=dados['nome'],
                    login=dados['login'],
                    senha=dados['senha'],
                    aeroporto_id=int(dados.get('aeroporto_id', 0)),
                    cpf=dados.get('cpf', '')
                )
            else:
                novo_usuario = Usuario(
                    nome=dados['nome'],
                    login=dados['login'],
                    senha=dados['senha']
                )
            
            self.usuario_dao.salvar(novo_usuario)
            return True, "Usuário cadastrado com sucesso!"

        except Exception as e:
            return False, f"Erro ao criar usuário: {str(e)}"

    def excluir(self, id_usuario: int):
        # Regra de segurança: Não permitir que o usuário se exclua
        # Por enquanto, apenas deleta.
        if self.usuario_dao.delete(id_usuario):
            return True, "Usuário excluído."
        return False, "Usuário não encontrado."