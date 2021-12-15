from __future__ import annotations
from typing import List, Optional, Type, TypeVar
from dataclasses import dataclass

T = TypeVar("T")

# The flag for if the game should be stopped
@dataclass
class GameOver: pass

# Represents a gameworld
class World:
    # The resources in the world
    _resources: List[any]
    # The entities in the world
    _entities: List[List[any]]
    # The dispatched events
    _events: List[Event]

    def __init__(self):
        self._resources = []
        self._entities = []
        self._events = []

    # Spawn an entity in the world and return it
    def spawn(self) -> List[any]:
        self._entities.append([])
        return self._entities[len(self._entities)-1]

    # Spawn a scene
    def spawn_scene(self, scene: Scene):
        self._entities.extend(scene.entities.copy())

    # Remove all entities
    def clear_entities(self):
        self._entities.clear()

    # Dispatch an event
    def dispatch_event(self, event: Event):
        self._events.append(event)

    # Insert a resource
    def insert_resource(self, resource: any):
        for i in range(len(self._resources)):
            r = self._resources[i]
            # Replace the resource if it already exists
            if isinstance(r, type(resource)):
                self._resources[i] = resource
                return
        self._resources.append(resource)

    # Get a resource
    def get_resource(self, type: Type[T]) -> Optional[T]:
        for resource in self._resources:
            if isinstance(resource, type):
                return resource
        return None

    # Query the world for entities with components
    def query(self, *types: Type[T]) -> List[any]:
        entities = []
        for i in range(len(self._entities)):
            entity = self._entities[i]
            components = []
            for type in types:
                # Add the entity id
                if type == Entity:
                    components.append(Entity(i))
                # Add the component of type
                for component in entity:
                    if isinstance(component, type):
                        components.append(component)
                        break
                if len(components) == len(types):
                    entities.append(components)
                    break
        return entities

    # Return the entities
    def get_entities(self) -> List[List[T]]:
        return self.entities

    # Save the world as a scene
    def to_scene(self) -> Scene:
        return Scene(self._entities.copy())

# The representation of an entity
@dataclass
class Entity:
    _id: int
    # Return the entity id
    def id(self):
        return self._id

# Represents an event
class Event: pass

# Represents a scene to be loaded
@dataclass
class Scene:
    # The entities in the scene
    entities: List[List[any]]

    def __str__(self) -> str:
        return self._entities.__str__()