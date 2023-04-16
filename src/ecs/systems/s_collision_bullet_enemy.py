import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)

    for bullet_entity, (c_s_b, c_t_b, _) in bullet_components:
        bullet_rect = c_s_b.surf.get_rect(topleft = c_t_b.pos)
        for enemy_entity, (c_s_e, c_t_e, _) in enemy_components:
            ene_rect = c_s_e.surf.get_rect(topleft = c_t_e.pos)

            if bullet_rect.colliderect(ene_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
               


         