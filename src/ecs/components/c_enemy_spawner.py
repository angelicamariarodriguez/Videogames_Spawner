import pygame

from src.read.spawn_event_data import SpawnEventData

class CEnemySpawner:
    def __init__(self, levels:str) -> None:
        spawnEventData = SpawnEventData(levels)
        events = spawnEventData.get_events()
        self.events = events
