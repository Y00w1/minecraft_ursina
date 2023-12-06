from ursina import Entity
from npc.npc_interface import NPC
from npc.npc_types_enum import NPCTypes
from npc.chicken import Chicken
from npc.skeleton import Skeleton


class NPCFactory:
    @staticmethod
    def create_npc(npc_type: NPCTypes, shootables_parent, position=None) -> NPC:
        if npc_type == NPCTypes.HOSTILE:
            npc = Skeleton(shootables_parent, position=position)
        elif npc_type == NPCTypes.PASSIVE:
            npc = Chicken(shootables_parent, position=position)
        else:
            raise ValueError("Invalid NPC type")

        return npc
    
class NPC(Entity, NPCFactory):
    def __init__(self, model, **kwargs):
        super().__init__(model=model, **kwargs)
        
    def get_npc(self):
        pass
