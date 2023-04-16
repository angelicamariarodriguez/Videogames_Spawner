import random
import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer

def create_square(world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                CSurface(size, col))
    world.add_component(cuad_entity,
                CTransform(pos))
    world.add_component(cuad_entity, 
                CVelocity(vel))
    return cuad_entity

def create_enemy_square(world:esper.World, pos:pygame.Vector2, enemy_info:dict):
    size = pygame.Vector2(enemy_info["size"]["x"], 
                          enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_square(world, size, pos, velocity, color)
    world.add_component(enemy_entity, CTagEnemy())

def create_player_square(world:esper.World, player_info:dict, player_lvl_info:dict) -> int:
    size = pygame.Vector2(player_info["size"]["x"], player_info["size"]["y"])
    color = pygame.Color(player_info["color"]["r"], player_info["color"]["g"], player_info["color"]["b"])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size.x /2), player_lvl_info["position"]["y"] - (size.y/2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_square(world, size, pos, vel, color)
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_enemy_spawner(world:esper.World, level_data:dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))

def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()
    world.add_component(input_left, 
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, 
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, 
                        CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, 
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))

def create_bullet_square(world:esper.World,
                        player_info:dict,
                        player_position:pygame.Vector2,
                        bullet_info:dict, click_position: pygame.Vector2):
    size = pygame.Vector2(bullet_info["size"]["x"],
                          bullet_info["size"]["y"])
    color = pygame.Color(bullet_info["color"]["r"],
                         bullet_info["color"]["g"],
                         bullet_info["color"]["b"])
    player_size_x = player_info["size"]["x"]
    player_size_y = player_info["size"]["y"]
    pos = pygame.Vector2(player_position.x + (player_size_x/2) - (size.x/2), player_position.y + (player_size_y/2) - (size.y/2))
    vel_x = click_position[0] - pos.x + size.x/2
    vel_y = click_position[1] - pos.y + size.y/2
    vel = pygame.Vector2(vel_x, vel_y)
    vel = vel.normalize() * bullet_info["velocity"]
    bullet_entity = create_square(world, size, pos, vel, color)
    world.add_component(bullet_entity, CTagBullet())