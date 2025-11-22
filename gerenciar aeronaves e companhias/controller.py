from modelo import CompanhiaAerea, Endereco, Aeronave
from persistence import CompanhiaDAO, EnderecoDAO, PilotoDAO, AeronaveDAO, VooDAO
from typing import cast, Optional

class ControladorCompanhia:
    def __init__(self):
        self.companhia_dao = CompanhiaDAO()
        self.endereco_dao = EnderecoDAO()
        self.piloto_dao = PilotoDAO()
        self.aeronave_dao = AeronaveDAO()

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

        if companhia.enderecoSede:
            self.endereco_dao.delete(companhia.enderecoSede.id)
        
        self.companhia_dao.delete(id_companhia)
        return True, "Companhia excluída com sucesso."


class ControladorAeronave:
    def __init__(self):
        self.aeronave_dao = AeronaveDAO()
        self.voo_dao = VooDAO()
        self.companhia_dao = CompanhiaDAO()

    def get_all_aeronaves(self):
        return self.aeronave_dao.get_all()
    
    def get_all_companhias(self):
        return self.companhia_dao.get_all()

    def validarDados(self, dadosAeronave):
        if not dadosAeronave.get('modelo'):
            return False, "Erro: O modelo da aeronave é obrigatório."
        if not dadosAeronave.get('companhia_id'):
            return False, "Erro: A companhia aérea é obrigatória."
        
        try:
            carga = float(dadosAeronave.get('capacidadeDeCarga', 0))
            lotacao = int(dadosAeronave.get('lotacaoMaxima', 0))
            if carga < 0 or lotacao < 0:
                 return False, "Erro: Valores não podem ser negativos."
        except ValueError:
            return False, "Erro: Capacidade e Lotação devem ser números válidos."
            
        return True, ""

    def _is_modelo_unico(self, modelo: str, id_atual: Optional[int] = None) -> bool:
        modelo_lower = modelo.lower()
        for aeronave in self.aeronave_dao.get_all():
            if aeronave.modelo.lower() == modelo_lower and aeronave.id != id_atual:
                return False
        return True

    def cadastrar(self, dadosAeronave):
        valido, msg = self.validarDados(dadosAeronave)
        if not valido:
            return None, msg

        modelo_aeronave = dadosAeronave.get('modelo', '')
        if not self._is_modelo_unico(modelo_aeronave):
            return None, f"Erro: Já existe uma aeronave com o modelo '{modelo_aeronave}'."

        comp_id = int(dadosAeronave['companhia_id'])
        
        dados_prontos = {
            'modelo': dadosAeronave['modelo'],
            'companhia_id': comp_id,
            'capacidadeDeCarga': float(dadosAeronave.get('capacidadeDeCarga', 0)),
            'lotacaoMaxima': int(dadosAeronave.get('lotacaoMaxima', 0)),
            'tipoDeAviao': dadosAeronave.get('tipoDeAviao', '')
        }
        
        aeronave = Aeronave.create(dados_prontos)

        aeronave_salva = self.aeronave_dao.salvar(aeronave)
        return aeronave_salva, "Aeronave salva com sucesso!"

    def atualizar(self, id_aeronave, dadosAeronave):
        valido, msg = self.validarDados(dadosAeronave)
        if not valido:
            return None, msg

        comp_id = int(dadosAeronave['companhia_id'])
        dadosAeronave['companhia_id'] = comp_id
        dadosAeronave['capacidadeDeCarga'] = float(dadosAeronave.get('capacidadeDeCarga', 0))
        dadosAeronave['lotacaoMaxima'] = int(dadosAeronave.get('lotacaoMaxima', 0))
        
        aeronave = self.aeronave_dao.get_by_id(id_aeronave)
        if not aeronave:
            return None, "Erro: Aeronave não encontrada."
        
        novo_modelo = dadosAeronave.get('modelo', '')
        if not self._is_modelo_unico(novo_modelo, id_atual=id_aeronave):
             return None, f"Erro: Já existe outra aeronave com o modelo '{novo_modelo}'."
        
        for key, value in dadosAeronave.items():
            setattr(aeronave, key, value)
        
        aeronave_atualizada = self.aeronave_dao.salvar(aeronave)
        return aeronave_atualizada, "Aeronave atualizada com sucesso!" 

    def excluir(self, id_aeronave):
        if self.voo_dao.existem_voos_para_aeronave(id_aeronave):
            return False, "Erro: Existem voos agendados para esta aeronave."
        
        if self.aeronave_dao.delete(id_aeronave):
            return True, "Aeronave excluída com sucesso."
        
        return False, "Erro: Aeronave não encontrada."