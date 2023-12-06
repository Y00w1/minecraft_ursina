from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class PlayerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PlayerSingleton, cls).__new__(cls)
            cls._instance._create_entity()
        return cls._instance

    def _create_entity(self):
        self.entity = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
        self.entity.collider = BoxCollider(self.entity, Vec3(0, 1, 0), Vec3(1, 2, 1))
