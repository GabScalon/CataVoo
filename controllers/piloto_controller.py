from persistent import PilotoDAO, VooDAO, CompanhiaAereaDAO
from model.piloto import Piloto

class PilotoController:
    def __init__(self):
        self.piloto_dao = PilotoDAO()
        self.voo_dao = VooDAO()
        self.companhia_dao = CompanhiaAereaDAO()

    def get_all_pilotos(self):
        return self.piloto_dao.get_all()
    
    def get_all_companhias(self):
        return self.companhia_dao.get_all()

    def cadastrar(self, dados):
        # Validações
        if not dados.get('nome'):
            return None, "Erro: Nome é obrigatório."
        if not dados.get('cpf'):
            return None, "Erro: CPF é obrigatório."
        if not dados.get('companhia_id'):
            return None, "Erro: Selecione uma companhia aérea."

        try:
            # Criação do Objeto
            novo_piloto = Piloto(
                nome=dados['nome'],
                companhia_id=int(dados['companhia_id']),
                cpf=dados['cpf'],
                codigoDeLicensa=dados.get('codigoDeLicensa', '')
            )
            
            # Persistência
            self.piloto_dao.salvar(novo_piloto)
            return True, "Piloto cadastrado com sucesso!"

        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"

    def atualizar(self, id_piloto, dados):
        piloto = self.piloto_dao.get_by_id(id_piloto)
        if not piloto:
            return False, "Erro: Piloto não encontrado."

        if not dados.get('nome') or not dados.get('cpf'):
            return False, "Erro: Nome e CPF são obrigatórios."

        try:
            piloto.nome = dados['nome']
            piloto.cpf = dados['cpf']
            piloto.codigoDeLicensa = dados.get('codigoDeLicensa', '')
            
            if 'companhia_id' in dados:
                piloto.companhia_id = int(dados['companhia_id'])

            self.piloto_dao.salvar(piloto)
            return True, "Piloto atualizado com sucesso!"

        except Exception as e:
            return False, f"Erro ao atualizar: {str(e)}"

    def excluir(self, id_piloto):
        # Verifica dependência de Voo (Não pode apagar piloto com voo marcado)
        # Como o VooDAO não tem um método específico "existem_voos_para_piloto", iteramos manualmente aqui.
        voos = self.voo_dao.get_all()
        for v in voos:
            if v.piloto_id == id_piloto:
                return False, "Erro: Este piloto tem voos agendados. Remova os voos antes de excluir o piloto."
        
        # Exclusão
        if self.piloto_dao.delete(id_piloto):
            return True, "Piloto excluído com sucesso."
        
        return False, "Erro: Piloto não encontrado."