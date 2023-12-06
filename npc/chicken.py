from ursina import *
from npc.npc_interface import NPC
from player import PlayerSingleton

player_singleton = PlayerSingleton()

class Chicken(NPC, Entity):
    def __init__(self, shootables_parent, **kwargs):
        super().__init__(model='npc/textures/chicken.fbx', parent=shootables_parent, collider='box', scale=0.06, double_sided = True,**kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.green, world_scale=(1.5, .1, .1))
        self.max_hp = 50
        self.hp = self.max_hp
        self.player = player_singleton.entity
        self.body_texture = load_texture('npc/textures/chicken.png')
        self.bill_texture = load_texture('npc/textures/chicken.png')
        self.texture = self.body_texture
        self.y = 0.3
        #self.bill_entity = Entity(parent=self, model='npc/textures/chicken.fbx', scale=(1.1, 1, 1), origin=(-0.5, 0.25, 0), texture=self.bill_texture)

    def update(self):
        player = self.player
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        if dist < 10:  # If player is within a certain range, run away
            move_speed = 6.0
            self.position -= self.forward * time.dt * move_speed

            # Optionally, you can add a random rotation to make them move more naturally
            self.rotation_y += random.uniform(-10, 10) * time.dt


    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return
        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1
    
    def get_npc(self):
        return self