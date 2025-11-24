from persistent import AeroportoDAO, VooDAO
from model.aeroporto import Aeroporto
from model.endereco import Endereco

class AeroportoController:
    def __init__(self):
        self.aeroporto_dao = AeroportoDAO()
        self.voo_dao = VooDAO()

    def get_all_aeroportos(self):
        return self.aeroporto_dao.get_all()

    def validar_dados(self, dados_aero, dados_end):
        if not dados_aero.get('nome'):
            return False, "Erro: Nome do aeroporto é obrigatório."
        if not dados_end.get('cidade') or not dados_end.get('estado'):
            return False, "Erro: Cidade e Estado são obrigatórios."
        return True, ""

    def _processar_portoes(self, texto_portoes: str):
        """Converte string 'A1, A2, B1' em lista ['A1', 'A2', 'B1']"""
        if not texto_portoes:
            return []
        return [p.strip() for p in texto_portoes.split(',') if p.strip()]

    def cadastrar(self, dados_aero, dados_end):
        valido, msg = self.validar_dados(dados_aero, dados_end)
        if not valido: return False, msg

        try:
            # Criar Endereço
            endereco = Endereco(
                rua=dados_end.get('rua', ''),
                numero=int(dados_end.get('numero', 0)),
                bairro=dados_end.get('bairro', ''),
                cidade=dados_end['cidade'],
                estado=dados_end['estado'],
                pais=dados_end.get('pais', 'Brasil')
            )

            # Criar Aeroporto
            portoes_lista = self._processar_portoes(dados_aero.get('portoes_str', ''))
            
            novo_aeroporto = Aeroporto(
                nome=dados_aero['nome'],
                endereco=endereco,
                ehPublico=dados_aero.get('ehPublico', True),
                portoes=portoes_lista
            )

            self.aeroporto_dao.salvar(novo_aeroporto)
            return True, "Aeroporto cadastrado com sucesso!"

        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"

    def atualizar(self, id_aero, dados_aero, dados_end):
        aeroporto = self.aeroporto_dao.get_by_id(id_aero)
        if not aeroporto: return False, "Aeroporto não encontrado."

        valido, msg = self.validar_dados(dados_aero, dados_end)
        if not valido: return False, msg

        try:
            # Atualiza dados básicos
            aeroporto.nome = dados_aero['nome']
            aeroporto.ehPublico = dados_aero['ehPublico']
            aeroporto.portoes = self._processar_portoes(dados_aero.get('portoes_str', ''))

            # Atualiza Endereço (Objeto interno)
            end = aeroporto.endereco
            end.rua = dados_end.get('rua', '')
            end.numero = int(dados_end.get('numero', 0))
            end.bairro = dados_end.get('bairro', '')
            end.cidade = dados_end['cidade']
            end.estado = dados_end['estado']
            end.pais = dados_end.get('pais', '')

            self.aeroporto_dao.salvar(aeroporto)
            return True, "Aeroporto atualizado com sucesso!"

        except Exception as e:
            return False, f"Erro ao atualizar: {str(e)}"

    def excluir(self, id_aero):
        # Verifica dependências em Voos (Origem ou Destino)
        voos = self.voo_dao.get_all()
        for v in voos:
            if v.localDeSaida_id == id_aero or v.destino_id == id_aero:
                return False, "Erro: Existem voos vinculados a este aeroporto (Origem ou Destino)."

        if self.aeroporto_dao.delete(id_aero):
            return True, "Aeroporto excluído com sucesso."
        return False, "Aeroporto não encontrado."