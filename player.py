from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
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
        self.max_player_health = 100
        self._create_health_bar()

    def get_player_health(self):
        return self.health_bar.value

    def _create_health_bar(self):
        self.health_bar = HealthBar(parent=camera.ui, value=self.max_player_health, position=(0, -0.45), world_scale=(0.2, 0.02))

    def update_health_bar(self, value):
        self.health_bar.value = value
        
    def get_max_player_health(self):
        return self.max_player_health

