from bot.storage import load_json, save_json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Store():
    path: str
    data: Dict[str, List[str]]

    @classmethod
    def load(cls, path):
        return cls(path=path, data=load_json(path, {}))

    def _key(self, gid):
        return str(gid)
    
    def list(self, gid):
        key = self._key(gid)

        if key not in self.data:
            self.data[key] = []

        return self.data[key]
    
    def add(self, gid, text):
        serverList = self.list(gid)

        if text in serverList:
            return False
        serverList.append(text)
        self.save()
        return True

    
    def clear(self, gid):
        self.list(gid).clear()
        self.save()
    
    def save(self):
        save_json(self.path, self.data)
