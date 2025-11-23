from typing import Optional
from persistent import AeronaveDAO, VooDAO, CompanhiaAereaDAO
from entities import Aeronave

class AeronaveController:
    def __init__(self):
        self.aeronave_dao = AeronaveDAO()
        self.voo_dao = VooDAO()
        self.companhia_dao = CompanhiaAereaDAO()

    def get_all_aeronaves(self):
        return self.aeronave_dao.get_all()
    
    def get_all_companhias(self):
        return self.companhia_dao.get_all()

    def _is_modelo_unico(self, modelo: str, id_atual: Optional[int] = None) -> bool:
        modelo_lower = modelo.lower()
        for aeronave in self.aeronave_dao.get_all():
            if aeronave.modelo.lower() == modelo_lower and aeronave.id != id_atual:
                return False
        return True

    def cadastrar(self, dadosAeronave):
        if not dadosAeronave.get('modelo'):
            return None, "Erro: O modelo da aeronave é obrigatório."
        if dadosAeronave.get('companhia_id') in ["", None]:
            return None, "Erro: A companhia aérea é obrigatória."

        modelo_aeronave = dadosAeronave.get('modelo', '')
        
        if not self._is_modelo_unico(modelo_aeronave):
            return None, f"Erro: Já existe uma aeronave com o modelo '{modelo_aeronave}'."

        try:
            comp_id = int(dadosAeronave['companhia_id'])
            carga = float(dadosAeronave.get('capacidadeDeCarga', 0))
            lotacao = int(dadosAeronave.get('lotacaoMaxima', 0))

            if carga < 0 or lotacao < 0:
                return None, "Erro: Capacidade e Lotação não podem ser negativas."

            dados_prontos = {
                'modelo': modelo_aeronave,
                'companhia_id': comp_id,
                'capacidadeDeCarga': carga,
                'lotacaoMaxima': lotacao,
                'tipoDeAviao': dadosAeronave.get('tipoDeAviao', '')
            }
            
            aeronave = Aeronave.create(dados_prontos)
            aeronave_salva = self.aeronave_dao.salvar(aeronave)
            
            return aeronave_salva, "Aeronave salva com sucesso!"

        except ValueError:
            return None, "Erro: Verifique se 'Capacidade' e 'Lotação' são números válidos."
        except Exception as e:
            return None, f"Erro inesperado ao cadastrar: {str(e)}"

    def atualizar(self, id_aeronave, dadosAeronave):
        aeronave = self.aeronave_dao.get_by_id(id_aeronave)
        if not aeronave:
            return None, "Erro: Aeronave não encontrada."

        if not dadosAeronave.get('modelo'):
            return None, "Erro: O modelo é obrigatório."
        
        novo_modelo = dadosAeronave.get('modelo', '')
        if not self._is_modelo_unico(novo_modelo, id_atual=id_aeronave):
             return None, f"Erro: Já existe outra aeronave com o modelo '{novo_modelo}'."

        try:
            aeronave.modelo = novo_modelo
            aeronave.tipoDeAviao = dadosAeronave.get('tipoDeAviao', '')
            
            if 'companhia_id' in dadosAeronave:
                aeronave.companhia_id = int(dadosAeronave['companhia_id'])
            
            if 'capacidadeDeCarga' in dadosAeronave:
                carga = float(dadosAeronave['capacidadeDeCarga'])
                if carga < 0: return None, "Erro: Carga não pode ser negativa."
                aeronave.capacidadeDeCarga = carga

            if 'lotacaoMaxima' in dadosAeronave:
                lotacao = int(dadosAeronave['lotacaoMaxima'])
                if lotacao < 0: return None, "Erro: Lotação não pode ser negativa."
                aeronave.lotacaoMaxima = lotacao
        
            aeronave_atualizada = self.aeronave_dao.salvar(aeronave)
            return aeronave_atualizada, "Aeronave atualizada com sucesso!" 

        except ValueError:
            return None, "Erro: Verifique se os valores numéricos estão corretos."
        except Exception as e:
            return None, f"Erro ao atualizar: {str(e)}"

    def excluir(self, id_aeronave):
        if self.voo_dao.existem_voos_para_aeronave(id_aeronave):
            return False, "Erro: Existem voos agendados para esta aeronave. Cancele os voos antes de excluir a aeronave."
        
        if self.aeronave_dao.delete(id_aeronave):
            return True, "Aeronave excluída com sucesso."
        
        return False, "Erro: Aeronave não encontrada."