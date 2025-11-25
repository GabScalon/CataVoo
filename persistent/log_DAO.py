from .base_DAO import PickleDAO
from model.log import LogSistema

class LogDAO(PickleDAO[LogSistema]):
    def __init__(self):
        super().__init__('db_logs.pkl')

    def buscar_por_filtro(self, termo="", data_inicio=None, data_fim=None):
        resultados = self.get_all()
        
        # Filtro por texto (nome do usuário ou ação)
        if termo:
            termo = termo.lower()
            resultados = [
                l for l in resultados 
                if termo in l.usuario_responsavel.lower() or termo in l.acao.lower() or termo in l.alvo.lower()
            ]
            
        # Filtro por data
        if data_inicio:
            resultados = [l for l in resultados if l.data_hora >= data_inicio]
        if data_fim:
            resultados = [l for l in resultados if l.data_hora <= data_fim]
            
        # Ordenar do mais recente para o mais antigo
        return sorted(resultados, key=lambda x: x.data_hora, reverse=True)