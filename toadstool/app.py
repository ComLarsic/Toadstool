from __future__ import annotations
from types import FunctionType
from typing import Dict, List, Type, TypeVar

from .world import GameOver, World, Event

T = TypeVar("T")

# Represents the app
class App:
    # The flag for if the app should run
    _should_run: bool
    # The gameworld
    _world: World
    # The systems in the world
    _startup_systems: List[FunctionType]
    _event_systems: Dict[str, List[FunctionType]]
    _systems: List[FunctionType]

    def __init__(self):
        self._should_run = True
        self._world = World()
        self._startup_systems = []
        self._event_systems = {}
        self._systems = []

    # Add a plugin
    def add_plugin(self, plugin: Plugin):
        plugin.build(self)

    # Add a startup system
    def add_startup_system(self, system: FunctionType):
        self._startup_systems.append(system)
    
    # Add an event system
    def add_event_system(self, event: Type, system: FunctionType):
        if str(event) in self._event_systems.keys():
            self._event_systems[str(event)].append(system)
            return
        self._event_systems[str(event)] = [system]

    # Add a system 
    def add_system(self, system: FunctionType):
        self._systems.append(system)
    
    # Call a system
    def call_system(self, system: FunctionType):
        system(self._world)
    
    # Dispatch an event
    def handle_event(self, event: Event):
        for system in self._event_systems[str(type(event))]:
            system(event, self._world)

    # Insert a resource
    def insert_resource(self, resource: any):
        self._world.insert_resource(resource)

    # Start the app
    def run(self):
        # Run startup systems
        for system in self._startup_systems:
            self.call_system(system)

        # The gameloop        
        while self._world.get_resource(GameOver) == None:
            # Run unbound systems
            for system in self._systems:
                self.call_system(system)
            # Handle events
            for event in self._world._events:
                self.handle_event(event)
            self._world._events.clear()

# To be inherited by every plugins
class Plugin:
    # Builds the app
    def build(self, app: App):
        pass