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
        if self.health_bar.value <= 0:
            self.handle_player_death()
        
    def get_max_player_health(self):
        return self.max_player_health
    
    def handle_player_death(self):
        self.disable_player_controls()
        self.display_death_message()

    def disable_player_controls(self):
        self.entity.enabled = False
        self.entity.visible_self = False
        self.entity.cursor.enabled = False
        # Disable the gun
        mouse.locked = False
        application.paused = True


    def display_death_message(self):
        # Create a Text entity
        self.death_message = Text(text='YOU LOSE!', world_scale=200, font='VeraMono.ttf', position=(0,0), origin=(0,0), color=color.red)
        # Create a "RESET" button
        self.reset_button = Button(text='RESET', color=color.green, position=(-0.1, -0.1), scale=(0.1, 0.05))
        #self.reset_button.on_click = self.reset_game 

        # Create a "QUIT" button
        self.quit_button = Button(text='QUIT', color=color.red, position=(0.1, -0.1), scale=(0.1, 0.05))
        self.quit_button.on_click = application.quit  # Quit the application when the button is clicked

