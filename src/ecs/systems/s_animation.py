import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world: esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)

    for _, (c_s, c_a) in components:
        # 1. Disminuir el valor de curr_time de la animacion
        c_a.curr_anim_time -= delta_time
        # 2. Cuando curr_time <= 0, hacemos cambio de frame
        if c_a.curr_anim_time <= 0:
            #Restaurar el tiempo
            c_a.curr_anim_time = c_a.animations_list[c_a.curr_anim].framerate
            c_a.curr_frame += 1
        # 3. Limitar el frame con sus propiedades de start y end
            if c_a.curr_frame > c_a.animations_list[c_a.curr_anim].end:
                c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start
        # 4. Calcular la nueva sub area del rectangulo de sprite
            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.curr_frame