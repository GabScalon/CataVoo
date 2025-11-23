import pickle
import os
from typing import TypeVar, Protocol, Optional, List, Generic, Dict

# Define o Protocolo (Interface) que obriga ter um ID
class HasId(Protocol):
    id: Optional[int]

# Define o Tipo Genérico T
T = TypeVar('T', bound=HasId)

class PickleDAO(Generic[T]):
    
    def __init__(self, filename: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        base_dir = os.path.join(base_dir, "dados")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Combina o caminho da pasta com o nome do arquivo
        self.filename = os.path.join(base_dir, filename)
        
        self.data: Dict[int, T] = self._load()

    def _load(self) -> Dict[int, T]:
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

    def get_all(self) -> List[T]:
        return list(self.data.values())

    def get_by_id(self, id: int) -> Optional[T]:
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