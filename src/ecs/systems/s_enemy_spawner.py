import esper
import pygame
from src.create.prefab_creator import create_cuad
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world:esper.World, conf_enemies:str):
    components= world.get_components(CEnemySpawner)

    c_s: CEnemySpawner
    

    for entity, (c_s) in components:
        
        
        for event in c_s[0].events:


            now = pygame.time.get_ticks() / 1000.0
            enemy_name = event[1]
            enemy_pos_x = event[2]['x']
            enemy_pos_y = event[2]['y']
            
            if event[3]==False and now >= event[0]:
                event[3] = True
                print(now)
                print(enemy_name)
                create_cuad(world, conf_enemies, enemy_name, pygame.Vector2(enemy_pos_x,enemy_pos_y))