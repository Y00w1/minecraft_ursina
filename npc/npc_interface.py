from abc import ABC, abstractmethod

class NPC(ABC):
    @abstractmethod
    def get_npc(self):
        pass