class Usuario:
    def __init__(self, login: str, nome: str, tipo: str):
        self.login = login
        self.nome = nome
        self.tipo = tipo

    def __repr__(self):
        return f"Usuario(login='{self.login}', nome='{self.nome}', tipo='{self.tipo}')"

