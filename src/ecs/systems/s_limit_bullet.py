import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_limit_bullet(world: esper.World, screen:pygame.Surface):

    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_t, c_s, _) in components:

        bullet_rect = CSurface.get_area_relative(c_s.area, c_t.pos)

        if bullet_rect.left < 0 or bullet_rect.right > screen_rect.width or bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)
                
