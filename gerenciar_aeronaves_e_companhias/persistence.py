import pickle
import os
from typing import TypeVar, Protocol, Optional, Any

class HasId(Protocol):
    id: Optional[int]

T = TypeVar('T', bound=HasId)

class PickleDAO:

    def __init__(self, filename):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    return pickle.load(f)
            except (pickle.UnpicklingError, EOFError, AttributeError, ImportError):
                return {}
        return {}

    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def get_all(self) -> list:
        return list(self.data.values())

    def get_by_id(self, id: int) -> Any:
        return self.data.get(id)

    def get_next_id(self) -> int:
        if not self.data:
            return 1 
        
        int_keys = [k for k in self.data.keys() if isinstance(k, int)]
        
        if not int_keys:
            return 1 
            
        return max(int_keys) + 1

    def save(self, obj: T) -> T:
        if obj.id is None:
            obj.id = self.get_next_id()
        
        self.data[obj.id] = obj
        self._save()
        return obj

    def salvar(self, obj: T) -> T:
        return self.save(obj)
    
    def delete(self, id: int) -> bool:
        if id in self.data:
            del self.data[id]
            self._save()
            return True
        return False


class EnderecoDAO(PickleDAO):
    def __init__(self, filename='db_enderecos.pkl'):
        super().__init__(filename)

class CompanhiaDAO(PickleDAO):
    def __init__(self, filename='db_companhias.pkl'):
        super().__init__(filename)

class AeronaveDAO(PickleDAO):
    def __init__(self, filename='db_aeronaves.pkl'):
        super().__init__(filename)
    
    def existem_aeronaves_por_companhia(self, companhia_id: int) -> bool:
        for aeronave in self.get_all():
            c_id = getattr(aeronave, 'companhia_id', getattr(aeronave, 'empresa_id', None))
            if c_id == companhia_id:
                return True
        return False

class PilotoDAO(PickleDAO):
    def __init__(self, filename='db_pilotos.pkl'):
        super().__init__(filename)
    
    def existem_pilotos_por_companhia(self, companhia_id: int) -> bool:
        for piloto in self.get_all():
            if hasattr(piloto, 'companhia_id') and piloto.companhia_id == companhia_id:
                return True
        return False

class VooDAO(PickleDAO):
    def __init__(self, filename='db_voos.pkl'):
        super().__init__(filename)
    
    def existem_voos_para_aeronave(self, aeronave_id: int) -> bool:
        for voo in self.get_all():
            if hasattr(voo, 'aeronave_id') and voo.aeronave_id == aeronave_id:
                return True
        return False