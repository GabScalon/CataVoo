import pickle
from model.usuario import Usuario

class UsuarioRepository:
    def __init__(self, file_path: str = "usuarios.pkl"):
        self.__file_path = file_path

    def __load_data(self) -> dict[str, Usuario]:
        try:
            with open(self.__file_path, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return {}

    def __save_data(self, data: dict[str, Usuario]):
        with open(self.__file_path, 'wb') as f:
            pickle.dump(data, f)

    def find_by_cpf(self, cpf: str) -> Usuario | None:
        data = self.__load_data()
        return data.get(cpf)

    def buscar_todos(self) -> list[Usuario]:
        return list(self.__load_data().values())

    def buscar_por_login(self, login: str) -> Usuario | None:
        """Busca sequencial por login."""
        usuarios = self.buscar_todos()
        for u in usuarios:
            if u.login == login:
                return u
        return None

    def save(self, usuario: Usuario):
        data = self.__load_data()
        data[usuario.cpf] = usuario
        self.__save_data(data)

    def delete_by_cpf(self, cpf: str) -> bool:
        data = self.__load_data()
        if cpf in data:
            del data[cpf]
            self.__save_data(data)
            return True
        return False