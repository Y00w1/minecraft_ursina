from ursina import *
from npc.npc_interface import NPC
from player import PlayerSingleton

player_singleton = PlayerSingleton()

class Skeleton(NPC, Entity):
    def __init__(self, shootables_parent, **kwargs):
        super().__init__(model='npc/textures/wither.fbx', parent=shootables_parent, double_sided = True, scale = 0.1, collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp
        self.player = player_singleton.entity
        self.body_texture = load_texture('npc/textures/wither.png')
        self.bill_texture = load_texture('npc/textures/wither.png')
        self.texture = self.body_texture
        self.y = 1
        self.attack_cooldown = 1
        self.on_cooldown = False
    
    def update(self):
        player=self.player
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return
    
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)
    
        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 50
            elif not self.on_cooldown:
                self.on_cooldown = True
                invoke(setattr, self, 'on_cooldown', False, delay = self.attack_cooldown)
                player_health = PlayerSingleton().get_player_health()
                if player_health > 0:
                    player_health -= 5
                    PlayerSingleton().update_health_bar(player_health)
    
    def get_shot(self):
        if self._hp <= 0:
            return
        move_distance = 2.0 
        self.position -= self.forward * move_distance
    
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
