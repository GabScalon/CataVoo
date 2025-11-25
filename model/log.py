from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class LogSistema:
    usuario_responsavel: str
    acao: str
    alvo: str
    detalhes: str
    data_hora: datetime = datetime.now()
    id: Optional[int] = None