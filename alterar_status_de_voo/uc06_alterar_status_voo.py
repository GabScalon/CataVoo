from typing import Dict, List
#  from entities import Usuario, Aeronave, Voo  TODO: Converter corretamente após corrigir a persistência em "db_voos"

# --- Modelos e Dados (Auto-contido) ---

class Usuario:
    """Representa um usuário do sistema."""
    def __init__(self, login: str, nome: str, tipo: str):
        self.login = login
        self.nome = nome
        self.tipo = tipo

class Aeronave:
    """Representa um modelo de aeronave."""
    def __init__(self, modelo: str):
        self.modelo = modelo

class Voo:
    """Representa as informações de um voo catalogado."""
    def __init__(self, codigo: str, status_inicial: str = "Programado"):
        self.codigo = codigo
        self.status = status_inicial
    
    def __repr__(self):
        return f"Voo(codigo='{self.codigo}', status='{self.status}')"

# "Banco de Dados" simulado com um voo já existente para o teste
db_voos: Dict[str, Voo] = {
    "AZ-2110": Voo("AZ-2110")
}

# --- Lógica do Caso de Uso ---

STATUS_VALIDOS: List[str] = ["Programado", "Embarcando", "Cancelado", "Atrasado", "Realizado"]

def alterar_status_voo(usuario_logado: Usuario, codigo_voo: str, novo_status: str):
    """
    [UC06] Permite que um usuário logado altere o status de um voo existente.
    """
    print(f"--- [UC06] {usuario_logado.nome} está alterando o voo {codigo_voo} para '{novo_status}' ---")
    
    voo = db_voos.get(codigo_voo)
    if not voo:
        raise ValueError(f"O voo com código '{codigo_voo}' não foi encontrado.")
    if novo_status not in STATUS_VALIDOS:
        raise ValueError(f"O status '{novo_status}' é inválido. Válidos são: {STATUS_VALIDOS}")

    voo.status = novo_status
    print(f"Status do voo {codigo_voo} alterado com sucesso.")
    return voo

# --- Demonstração ---

if __name__ == "__main__":
    print("=====================================================")
    print("Executando demonstração do UC06: Alterar Status de Voo")
    print("=====================================================\n")

    # Simula um usuário que já passou pela autenticação
    usuario_logado = Usuario("func1", "João Silva", "Funcionário")
    
    voo_de_teste = "AZ-2110"

    print(f"Status ANTES da alteração: {db_voos[voo_de_teste]}")
    print("-" * 20)

    # Cenário 1: Alterar para um status válido
    try:
        alterar_status_voo(usuario_logado, voo_de_teste, "Atrasado")
    except ValueError as e:
        print(f"Falha na alteração: {e}")
    
    print("-" * 20)
    
    # Cenário 2: Tentar alterar para um status inválido
    try:
        alterar_status_voo(usuario_logado, voo_de_teste, "Em Manutenção")
    except ValueError as e:
        print(f"Falha na alteração: {e}")

    print(f"\nStatus DEPOIS das operações: {db_voos[voo_de_teste]}")