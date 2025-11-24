import re
from model.dto import CadastroUsuarioDTO, AlteracaoUsuarioDTO
from model.usuario import Usuario
from model.funcionario import Funcionario
from model.administrador import Administrador
from persistent import UsuarioRepository 
from utils.security import SecurityUtils

class UsuarioController:

    def __init__(self, repository: UsuarioRepository):
        self.__repository = repository

    def listar_todos(self):
        """Método público para acessar a lista de usuários sem quebrar o encapsulamento."""
        return self.__repository.buscar_todos()

    def __validar_cpf_completo(self, cpf: str) -> bool:
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            return False

        # 2. Lógica de validação dos dígitos
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def autenticar(self, login, senha_input):
        usuario = self.__repository.buscar_por_login(login)
        if not usuario:
            return None
        
        # Verifica se o hash bate
        if SecurityUtils.verificar_senha(senha_input, usuario.salt, usuario.senha_hash):
            return usuario
        return None

    def definir_nova_senha(self, cpf, nova_senha_plana):
        """Atualiza a senha do usuário e remove a flag de primeiro acesso."""
        usuario = self.__repository.find_by_cpf(cpf)
        if not usuario:
            return False

        novo_salt = SecurityUtils.gerar_salt()
        novo_hash = SecurityUtils.gerar_hash(nova_senha_plana, novo_salt)

        usuario.atualizar_senha(novo_hash, novo_salt)
        usuario.confirmar_primeiro_acesso()
        
        self.__repository.save(usuario)
        return True

    def cadastrar_usuario(self, dto: CadastroUsuarioDTO) -> tuple[str, str]:
        # Validações
        if not dto.nome or not dto.email or not dto.login:
            return ("ERRO", "Preencha Nome, Email e Login.")

        if self.__repository.find_by_cpf(dto.cpf):
            return ("ERRO", "CPF já cadastrado.")
            
        if self.__repository.buscar_por_login(dto.login):
            return ("ERRO", "Login já em uso.")

        try:
            # 1. Gerar senha temporária (apenas números do CPF)
            senha_temp = re.sub(r'\D', '', dto.cpf) 
            
            # 2. Criptografar
            salt = SecurityUtils.gerar_salt()
            senha_hash = SecurityUtils.gerar_hash(senha_temp, salt)

            # 3. Criar Objeto
            if dto.tipo_usuario == "FUNCIONARIO":
                novo = Funcionario(dto.cpf, dto.nome, dto.email, dto.login, senha_hash, salt, primeiro_acesso=True)
            elif dto.tipo_usuario == "ADMINISTRADOR":
                novo = Administrador(dto.cpf, dto.nome, dto.email, dto.login, senha_hash, salt, primeiro_acesso=True)
            else:
                return ("ERRO", "Tipo inválido.")
            
            self.__repository.save(novo)
            return ("SUCESSO", f"Usuário criado!\nLogin: {dto.login}\nSenha Inicial: {senha_temp} (CPF sem pontos)")
            
        except Exception as e:
            return ("ERRO", f"Erro ao salvar: {e}")

    # --- Métodos de validação e auxiliares ---
    def checar_status_cpf(self, cpf: str) -> tuple[str, str | Usuario]:
        cpf_limpo = cpf.strip()
        if not self.__validar_cpf_completo(cpf_limpo):
            return ('ERRO', f"CPF '{cpf}' é inválido ou mal formatado (use xxx.xxx.xxx-xx)")
        usuario = self.__repository.find_by_cpf(cpf_limpo)
        if usuario:
            return ("ENCONTRADO", usuario)
        else:
            return ("NAO_ENCONTRADO", cpf_limpo)

    def alterar_usuario(self, cpf, dto):
        usuario = self.__repository.find_by_cpf(cpf)
        if not usuario: return ("ERRO", "Usuário não encontrado.")
        usuario.nome = dto.nome
        usuario.email = dto.email
        self.__repository.save(usuario)
        return ("SUCESSO", "Dados atualizados.")

    def excluir_usuario(self, cpf):
        if self.__repository.delete_by_cpf(cpf):
            return ("SUCESSO", "Usuário excluído.")
        return ("ERRO", "Falha ao excluir.")