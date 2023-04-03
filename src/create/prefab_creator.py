import esper
import pygame
import json
import random
from src.ecs.components.c_enemy_spawner import CEnemySpawner

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def create_cuad(ecs_world:esper.World, conf_enemies:str, enemy_name:str, pos:pygame.Vector2):
        
        f = open(conf_enemies)
        enemies = json.load(f)
        enemy = enemies[enemy_name]
        size = enemy['size']
        color = enemy['color']
        velocity_min = enemy['velocity_min']
        velocity_max = enemy['velocity_max']
        vel_x = random.randint(velocity_min,velocity_max)*random.choice([1,-1])
        vel_y = random.randint(velocity_min,velocity_max)*random.choice([1,-1])
        
        cuad_entity = ecs_world.create_entity()
        ecs_world.add_component(cuad_entity, 
                        CSurface(pygame.Vector2(size['x'],size['y']), 
                                 pygame.Color(color['r'],color['g'],color['b'])))
        ecs_world.add_component(cuad_entity,
                        CTransform(pos))
        ecs_world.add_component(cuad_entity,
                         CVelocity(pygame.Vector2(pygame.Vector2(vel_x,vel_y))))

def create_spawner(ecs_world:esper.World, levels:str):
        spa_entity = ecs_world.create_entity()
        ecs_world.add_component(spa_entity, CEnemySpawner(levels))
