from typing import Optional
from persistent import CompanhiaAereaDAO, AeronaveDAO, PilotoDAO, EnderecoDAO
from entities import CompanhiaAerea, Endereco

class ControladorCompanhia:
    def __init__(self):
        self.companhia_dao = CompanhiaAereaDAO()
        self.aeronave_dao = AeronaveDAO()
        self.piloto_dao = PilotoDAO()
        self.endereco_dao = EnderecoDAO()

    def get_all_companhias(self):
        return self.companhia_dao.get_all()

    def validarDados(self, dadosCompanhia, dadosEndereco):
        if not dadosCompanhia.get('nome'):
            return False, "Erro: O nome da companhia é obrigatório."
        
        if not dadosEndereco.get('rua') or not dadosEndereco.get('cidade'):
            return False, "Erro: Rua e Cidade do endereço são obrigatórios."
        
        numero = dadosEndereco.get('numero', '')
        if str(numero) and not str(numero).isdigit():
             return False, "Erro: O número do endereço deve ser um valor inteiro."
             
        return True, ""

    def _is_nome_unico(self, nome: str, id_atual: Optional[int] = None) -> bool:
        nome_lower = nome.lower()
        for comp in self.companhia_dao.get_all():
            if comp.nome.lower() == nome_lower and comp.id != id_atual:
                return False
        return True

    def cadastrar(self, dadosCompanhia, dadosEndereco):
        valido, msg = self.validarDados(dadosCompanhia, dadosEndereco)
        
        if not valido:
            return None, msg

        nome_comp = dadosCompanhia.get('nome', '')
        if not self._is_nome_unico(nome_comp):
            return None, f"Erro: Já existe uma companhia com o nome '{nome_comp}'."

        dadosEnderecoConvertido = dadosEndereco.copy()
        try:
            num_str = str(dadosEndereco.get('numero', '0'))
            dadosEnderecoConvertido['numero'] = int(num_str) if num_str.isdigit() else 0
        except ValueError:
            dadosEnderecoConvertido['numero'] = 0

        novaCompanhia = CompanhiaAerea.create(dadosCompanhia)
        novoEndereco = Endereco.create(dadosEnderecoConvertido)
        
        enderecoSalvo = self.endereco_dao.salvar(novoEndereco)
        novaCompanhia.setEndereco(enderecoSalvo)
        
        companhiaSalva = self.companhia_dao.salvar(novaCompanhia)
        
        return companhiaSalva, "Companhia salva com sucesso!"

    def atualizar(self, id_companhia, dadosCompanhia, dadosEndereco):
        valido, msg = self.validarDados(dadosCompanhia, dadosEndereco)
        if not valido:
            return None, msg
        
        companhia = self.companhia_dao.get_by_id(id_companhia)
        if not companhia:
            return None, "Erro: Companhia não encontrada."
        
        novo_nome = dadosCompanhia.get('nome', '')
        if not self._is_nome_unico(novo_nome, id_atual=id_companhia):
             return None, f"Erro: Já existe outra companhia com o nome '{novo_nome}'."
        
        try:
            num_str = str(dadosEndereco.get('numero', '0'))
            dadosEndereco['numero'] = int(num_str) if num_str.isdigit() else 0
        except:
            dadosEndereco['numero'] = 0

        endereco = companhia.enderecoSede
        if endereco:
            for key, value in dadosEndereco.items():
                setattr(endereco, key, value)
            self.endereco_dao.salvar(endereco)
        
        for key, value in dadosCompanhia.items():
            setattr(companhia, key, value)
        
        companhia_atualizada = self.companhia_dao.salvar(companhia)
        
        return companhia_atualizada, "Companhia atualizada com sucesso!"

    def excluir(self, id_companhia):
        if self.piloto_dao.existem_pilotos_por_companhia(id_companhia):
            return False, "Erro: Existem pilotos ativos cadastrados nesta companhia."
        
        if self.aeronave_dao.existem_aeronaves_por_companhia(id_companhia):
            return False, "Erro: Existem aeronaves cadastradas nesta companhia. Remova-as ou edite-as antes de excluir a companhia."
        
        companhia = self.companhia_dao.get_by_id(id_companhia)
        if not companhia:
            return False, "Erro: Companhia não encontrada."

        if companhia.enderecoSede and companhia.enderecoSede.id is not None:
            self.endereco_dao.delete(companhia.enderecoSede.id)
        
        self.companhia_dao.delete(id_companhia)
        return True, "Companhia excluída com sucesso."