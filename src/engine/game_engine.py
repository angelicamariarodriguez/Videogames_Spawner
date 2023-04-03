import pygame
import esper
import json
from src.create.prefab_creator import create_cuad, create_spawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.read.spawn_event_data import SpawnEventData

class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        f = open('window.json')
        window = json.load(f)
        title = window['title']
        size = window['size']
        self.color = window['bg_color']
        self.screen = pygame.display.set_mode((size['w'], size['h']), pygame.SCALED)  
        pygame.display.set_caption(title)    
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = window['framerate']
        self.delta_time = 0
        self.ecs_world = esper.World()
        self.levels_file = 'level_01.json'
        self.enemies_conf_file = 'enemies.json'


        

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_spawner(self.ecs_world, self.levels_file)


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies_conf_file)

        


    def _draw(self):
        self.screen.fill((self.color['r'], self.color['g'], self.color['b']))
        system_rendering(self.ecs_world,self.screen)
        pygame.display.flip()
    

    def _clean(self):
        pygame.quit()
