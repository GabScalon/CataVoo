import hashlib
import secrets

class SecurityUtils:
    @staticmethod
    def gerar_salt() -> str:
        """Gera uma string aleatória (salt) para tornar o hash único."""
        return secrets.token_hex(16)

    @staticmethod
    def gerar_hash(senha_plana: str, salt: str) -> str:
        """Cria o hash da senha usando SHA-256 + Salt."""
        combinacao = salt + senha_plana
        return hashlib.sha256(combinacao.encode()).hexdigest()

    @staticmethod
    def verificar_senha(senha_input: str, salt_armazenado: str, hash_armazenado: str) -> bool:
        """Recalcula o hash e compara com o guardado."""
        hash_input = SecurityUtils.gerar_hash(senha_input, salt_armazenado)
        return hash_input == hash_armazenado