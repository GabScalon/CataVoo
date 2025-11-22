import datetime
from typing import Dict
#  from entities import Usuario, Aeronave, Voo TODO: Fazer a importação corretamente após implementar a persistência correta

# --- Modelos e Dados (Auto-contido) ---

class Usuario:
    """Representa um usuário do sistema."""
    def __init__(self, login: str, nome: str, tipo: str):
        self.login = login
        self.nome = nome
        self.tipo = tipo

class Aeronave:
    """Representa um modelo de aeronave com suas capacidades."""
    def __init__(self, modelo: str, lotacao_maxima: int):
        self.modelo = modelo
        self.lotacao_maxima = lotacao_maxima

class Voo:
    """Representa as informações de um voo catalogado."""
    def __init__(self, codigo: str, horario_partida: datetime.datetime, aeronave: Aeronave, num_passageiros: int):
        self.codigo = codigo
        self.horario_partida = horario_partida
        self.aeronave = aeronave
        self.numero_passageiros = num_passageiros
        self.status = "Programado"
    
    def __repr__(self):
        return f"Voo(codigo='{self.codigo}', status='{self.status}', passageiros={self.numero_passageiros})"

# "Banco de Dados" simulado para o caso de uso
db_aeronaves: Dict[str, Aeronave] = { "B737": Aeronave("Boeing 737", lotacao_maxima=162) }
db_voos: Dict[str, Voo] = {}

# --- Lógica do Caso de Uso ---

def cadastrar_voo(usuario_logado: Usuario, codigo: str, horario_partida: datetime.datetime, 
                  horario_chegada: datetime.datetime, modelo_aeronave: str, 
                  numero_passageiros: int):
    """
    [UC01] Permite que um usuário logado cadastre um novo voo, validando as regras de negócio.
    """
    print(f"--- [UC01] {usuario_logado.nome} está tentando cadastrar o voo {codigo} ---")
    
    if codigo in db_voos:
        raise ValueError(f"Erro [RN01]: O código de voo '{codigo}' já existe.")
    if horario_chegada <= horario_partida:
        raise ValueError("[RN02]: O horário de chegada não pode ser anterior ou igual ao de partida.")
    aeronave = db_aeronaves.get(modelo_aeronave)
    if not aeronave:
        raise ValueError(f"O modelo de aeronave '{modelo_aeronave}' não foi encontrado.")
    if numero_passageiros > aeronave.lotacao_maxima:
        raise ValueError(f"[RN03]: Número de passageiros ({numero_passageiros}) excede a capacidade ({aeronave.lotacao_maxima}).")

    novo_voo = Voo(codigo, horario_partida, aeronave, numero_passageiros)
    db_voos[codigo] = novo_voo
    print(f"Voo {codigo} cadastrado com sucesso!")
    return novo_voo

# --- Demonstração ---

if __name__ == "__main__":
    print("=====================================================")
    print("Executando demonstração do UC01: Cadastrar Voo")
    print("=====================================================\n")

    # Simula um usuário que já passou pela autenticação
    usuario_logado = Usuario("func1", "João Silva", "Funcionário")

    # Cenário 1: Cadastrar um voo válido
    try:
        horario_p = datetime.datetime(2025, 10, 20, 14, 30)
        horario_c = datetime.datetime(2025, 10, 20, 16, 45)
        cadastrar_voo(usuario_logado, "G3-1400", horario_p, horario_c, "B737", 150)
    except ValueError as e:
        print(f"Falha no cadastro: {e}")

    print("-" * 20)

    # Cenário 2: Tentar cadastrar um voo com excesso de passageiros (viola RN03)
    try:
        horario_p = datetime.datetime(2025, 11, 5, 10, 0)
        horario_c = datetime.datetime(2025, 11, 5, 12, 15)
        cadastrar_voo(usuario_logado, "LA-3020", horario_p, horario_c, "B737", 200)
    except ValueError as e:
        print(f"Falha no cadastro: {e}")

    print("\nEstado final do 'banco de dados' de voos:")
    print(db_voos)