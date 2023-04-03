import pygame
import json

class SpawnEventData:
    def __init__(self, levels:str) -> None:
        self.levels = levels
    
    def get_events(self):
        f = open(self.levels)
        levels = json.load(f)
        spawn_events = levels['enemy_spawn_events']
        events = []
        for event in spawn_events:
            events.append([event['time'], event['enemy_type'], event['position'], False])
        return events
    
        


   
        



