import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_hunter_state import CHunterState, HunterState


def system_hunter_state(world:esper.World, player_entity:int, hunter_info:dict):
    pl_t = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CHunterState, CAnimation, CTransform, CVelocity)
    for _, (c_hst, c_a, c_t, c_v) in components:
        if c_hst.state == HunterState.IDLE:
            _do_enemy_hunter_idle(c_hst, c_a, c_t, c_v, pl_t, hunter_info)
        elif c_hst.state == HunterState.CHASE:
            _do_enemy_hunter_chase(c_hst, c_a, c_t, c_v, pl_t, hunter_info)
        elif c_hst.state == HunterState.RETURN:
            _do_enemy_hunter_return(c_hst, c_a, c_t, c_v, hunter_info)


def _do_enemy_hunter_idle(c_hst:CHunterState, c_a:CAnimation, c_t:CTransform,
                          c_v:CVelocity, pl_t:CTransform, hunter_info:dict):
    _set_animation(c_a, 1)
    c_v.vel.x = 0
    c_v.vel.y = 0

    dist_to_player = c_t.pos.distance_to(pl_t.pos)
    if dist_to_player < hunter_info["distance_start_chase"]:
        c_hst.state = HunterState.CHASE


def _do_enemy_hunter_chase(c_hst:CHunterState, c_a:CAnimation, c_t:CTransform,
                           c_v:CVelocity, pl_t:CTransform, hunter_info:dict):
    _set_animation(c_a, 0)
    c_v.vel = (pl_t.pos - c_t.pos).normalize() * hunter_info["velocity_chase"]
    dist_to_start_point = c_hst.start_pos.distance_to(c_t.pos)
    if dist_to_start_point >= hunter_info["distance_start_return"]:
        c_hst.state = HunterState.RETURN


def _do_enemy_hunter_return(c_hst:CHunterState, c_a:CAnimation,
                            c_t:CTransform, c_v:CVelocity, hunter_info:dict):
    _set_animation(c_a, 0)
    c_v.vel = (c_hst.start_pos - c_t.pos).normalize() * hunter_info["velocity_return"]
    dist_to_origin = c_hst.start_pos.distance_to(c_t.pos)
    if dist_to_origin <= 2:
        c_t.pos.xy = c_hst.start_pos.xy
        c_hst.state = HunterState.IDLE

def _set_animation(c_a:CAnimation, num_anim:int):
    if c_a.curr_anim == num_anim:
        return
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start