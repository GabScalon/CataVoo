from datetime import datetime
from typing import List, Optional, Tuple

from persistent import VooDAO, AeronaveDAO, AeroportoDAO, CompanhiaAereaDAO, PilotoDAO
from entities import Voo

class VooController:
    def __init__(self):
        self.voo_dao = VooDAO()
        self.aeronave_dao = AeronaveDAO()
        self.aeroporto_dao = AeroportoDAO()
        self.companhia_dao = CompanhiaAereaDAO()
        self.piloto_dao = PilotoDAO()

    def buscar_todos(self) -> List[Voo]:
        return self.voo_dao.get_all()

    def buscar_por_codigo(self, codigo: str) -> List[Voo]:
        return self.voo_dao.buscar_por_codigo(codigo)

    def buscar_por_destino(self, aeroporto_id: int) -> List[Voo]:
        return self.voo_dao.buscar_por_destino(aeroporto_id)
    
    def get_aeroportos_para_combo(self):
        """Retorna lista de aeroportos para preencher comboboxes na view."""
        return self.aeroporto_dao.get_all()
        
    def get_aeronaves_para_combo(self):
        return self.aeronave_dao.get_all()
        
    def get_companhias_para_combo(self):
        return self.companhia_dao.get_all()
        
    def get_pilotos_para_combo(self):
        return self.piloto_dao.get_all()

    def _validar_horarios(self, partida: datetime, chegada: datetime) -> Tuple[bool, str]:
        """RN02: O horário de chegada não pode ser anterior ao de partida."""
        if chegada <= partida:
            return False, "Erro: O horário de chegada deve ser posterior à partida."
        return True, ""

    def _validar_capacidade(self, aeronave_id: int, passageiros: int) -> Tuple[bool, str]:
        """RN03: O número de passageiros não pode ultrapassar a lotação da aeronave."""
        capacidade_max = self.aeronave_dao.get_capacidade(aeronave_id)
        if passageiros > capacidade_max:
            return False, f"Erro: Passageiros ({passageiros}) excedem a lotação da aeronave ({capacidade_max})."
        return True, ""

    def _is_codigo_unico(self, codigo: str, id_atual: Optional[int] = None) -> bool:
        """RN01: Cada voo deve possuir um código único."""
        # Nota: O VooDAO já tem buscar_por_codigo, mas precisamos verificar ID para edição
        voos_com_codigo = self.voo_dao.buscar_por_codigo(codigo)
        for voo in voos_com_codigo:
            if voo.codigo.upper() == codigo.upper() and voo.id != id_atual:
                return False
        return True

    def cadastrar(self, dados_voo: dict):
        # 1. Validar campos obrigatórios
        campos_obrigatorios = ['codigo', 'aeronave_id', 'companhia_id', 
                             'piloto_id', 'localDeSaida_id', 'destino_id',
                             'horarioDePartidaPrevisto', 'horarioDeChegadaPrevisto']
        for campo in campos_obrigatorios:
            if campo not in dados_voo or not dados_voo[campo]:
                 return None, f"Erro: O campo {campo} é obrigatório."

        # 2. Validar Código Único (RN01)
        if not self._is_codigo_unico(dados_voo['codigo']):
            return None, f"Erro: O código de voo '{dados_voo['codigo']}' já existe."

        try:
            # Conversão segura de tipos
            aeronave_id = int(dados_voo['aeronave_id'])
            passageiros = int(dados_voo.get('numeroDePassageiros', 0))
            partida = dados_voo['horarioDePartidaPrevisto'] # Assume que já vem como datetime da View
            chegada = dados_voo['horarioDeChegadaPrevisto']

            # 3. Validar Horários (RN02)
            valido_hora, msg_hora = self._validar_horarios(partida, chegada)
            if not valido_hora:
                return None, msg_hora

            # 4. Validar Capacidade (RN03)
            valido_cap, msg_cap = self._validar_capacidade(aeronave_id, passageiros)
            if not valido_cap:
                return None, msg_cap

            # Criar objeto Voo
            # Convertendo IDs para inteiro para garantir
            novo_voo = Voo(
                codigo=dados_voo['codigo'],
                aeronave_id=aeronave_id,
                companhia_id=int(dados_voo['companhia_id']),
                piloto_id=int(dados_voo['piloto_id']),
                localDeSaida_id=int(dados_voo['localDeSaida_id']),
                destino_id=int(dados_voo['destino_id']),
                horarioDePartidaPrevisto=partida,
                horarioDeChegadaPrevisto=chegada,
                numeroDePassageiros=passageiros,
                carga=float(dados_voo.get('carga', 0.0)),
                statusDoVoo="Programado",
                portao=dados_voo.get('portao', '')
            )

            self.voo_dao.salvar(novo_voo)
            return novo_voo, "Voo cadastrado com sucesso!"

        except ValueError as e:
            return None, f"Erro de conversão de dados: {str(e)}"
        except Exception as e:
            return None, f"Erro inesperado: {str(e)}"

    def atualizar(self, id_voo: int, dados_voo: dict):
        voo = self.voo_dao.get_by_id(id_voo)
        if not voo:
            return None, "Erro: Voo não encontrado."

        # Validação de código único na edição
        novo_codigo = dados_voo.get('codigo', voo.codigo)
        if not self._is_codigo_unico(novo_codigo, id_atual=id_voo):
            return None, f"Erro: O código '{novo_codigo}' já está em uso."

        try:
            # Se houver alteração de aeronave ou passageiros, revalidar RN03
            nova_aeronave_id = int(dados_voo.get('aeronave_id', voo.aeronave_id))
            novos_passageiros = int(dados_voo.get('numeroDePassageiros', voo.numeroDePassageiros))
            
            valido_cap, msg_cap = self._validar_capacidade(nova_aeronave_id, novos_passageiros)
            if not valido_cap:
                return None, msg_cap

            # Se houver alteração de horários, revalidar RN02
            nova_partida = dados_voo.get('horarioDePartidaPrevisto', voo.horarioDePartidaPrevisto)
            nova_chegada = dados_voo.get('horarioDeChegadaPrevisto', voo.horarioDeChegadaPrevisto)
            
            valido_hora, msg_hora = self._validar_horarios(nova_partida, nova_chegada)
            if not valido_hora:
                return None, msg_hora

            # Atualiza os campos
            voo.codigo = novo_codigo
            voo.aeronave_id = nova_aeronave_id
            voo.companhia_id = int(dados_voo.get('companhia_id', voo.companhia_id))
            voo.piloto_id = int(dados_voo.get('piloto_id', voo.piloto_id))
            voo.localDeSaida_id = int(dados_voo.get('localDeSaida_id', voo.localDeSaida_id))
            voo.destino_id = int(dados_voo.get('destino_id', voo.destino_id))
            voo.horarioDePartidaPrevisto = nova_partida
            voo.horarioDeChegadaPrevisto = nova_chegada
            voo.numeroDePassageiros = novos_passageiros
            
            if 'carga' in dados_voo:
                voo.carga = float(dados_voo['carga'])
            if 'statusDoVoo' in dados_voo:
                voo.statusDoVoo = dados_voo['statusDoVoo']
            if 'portao' in dados_voo:
                voo.portao = dados_voo['portao']

            self.voo_dao.salvar(voo)
            return voo, "Voo atualizado com sucesso!"

        except Exception as e:
            return None, f"Erro ao atualizar voo: {str(e)}"

    def alterar_status(self, id_voo: int, novo_status: str):
        """UC06 - Alterar Status"""
        voo = self.voo_dao.get_by_id(id_voo)
        if not voo:
            return False, "Voo não encontrado."
            
        status_validos = ["Programado", "Embarcando", "Cancelado", "Atrasado", "Realizado", "Voando"]
        if novo_status not in status_validos:
             return False, f"Status inválido. Use: {', '.join(status_validos)}"
             
        voo.statusDoVoo = novo_status
        self.voo_dao.salvar(voo)
        return True, f"Status alterado para '{novo_status}'."

    def excluir(self, id_voo: int):
        if self.voo_dao.delete(id_voo):
            return True, "Voo excluído com sucesso."
        return False, "Erro: Voo não encontrado."