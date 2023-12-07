from ursina import *
from npc.npc_interface import NPC
from player import PlayerSingleton
from math import atan2, degrees, sqrt

player_singleton = PlayerSingleton()

class Chicken(NPC, Entity):
    def __init__(self, shootables_parent, **kwargs):
        super().__init__(model='npc/textures/chicken.fbx', parent=shootables_parent, collider='box', scale=0.06, double_sided=True, **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.green, world_scale=(1.5, .1, .1))
        self.max_hp = 50
        self.hp = self.max_hp
        self.player = player_singleton.entity
        self.body_texture = load_texture('npc/textures/chicken.png')
        self.bill_texture = load_texture('npc/textures/chicken.png')
        self.texture = self.body_texture
        self.y = 0.3
        self.move_speed = 30.0
        self.rotation_interval = random.uniform(3, 5)  # Random interval for rotation
        self.rotation_timer = 0.0
        self.shot_flag = False  # Flag to indicate if the chicken has been shot

    def update(self):
        player = self.player
        dist = distance_xz(player.position, self.position)

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        # Check if the chicken has been shot
        if self.shot_flag:
            self.position -= self.forward * time.dt * self.move_speed

            # Rotate away from the player
            direction_to_player = player.position - self.position
            angle_to_player = atan2(direction_to_player.x, direction_to_player.z)
            self.rotation_y = degrees(angle_to_player)

            self.rotation_timer = 0.0  # Reset rotation timer
        else:
            # Move straight
            self.position += self.forward * time.dt * self.move_speed

            # Increment rotation timer
            self.rotation_timer += time.dt

            # Check if it's time to rotate
            if self.rotation_timer >= self.rotation_interval:
                self.rotation_y += random.uniform(-180, 180)  # Rotate randomly
                self.rotation_interval = random.uniform(3, 5)  # Set a new random interval
                self.rotation_timer = 0.0  # Reset rotation timer

    def get_shot(self):
        self.shot_flag = True
        invoke(setattr, self, 'shot_flag', False, delay=0.5)


    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            player_health = PlayerSingleton().get_player_health()
            if player_health is not None:
                player_health += 20
                max_health = player_singleton.get_max_player_health()
                player_health = min(player_health, max_health)
                player_singleton.update_health_bar(player_health)
            
            destroy(self)
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
    
    def get_npc(self):
        return self