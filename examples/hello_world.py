"""
An example of how to spawn entities and access components.

Entities are represented internally as just arrays of components
---
# The internal representation of entities
self.entities: List[any] = []
---

Components can be defined as any class, but for simplicity we use dataclasses
---
# Both can be added as components

class ClassComponent:
    data: any

# It is reccomended to use dataclasses for simplicity
@dataclass
class DataComponent:
    data: any
---

Systems are just functions that take a world as an argument:
---
# A system that prints hello world
def hello_world(world: World):
    print("Hello, world!")
---
"""
from dataclasses import dataclass
from toadstool import App, World, Entity

# A component that represents an entities name
@dataclass
class Name:
    value: str

# A component that acts as a tag that tells the system to greet the entity
class Greeted: pass

# Setup the scene witrh entities
def setup(world: World):
    # Spawn an entity and add the components
    # Since entities are just represented as lists of components we can just append them
    entity_1 = world.spawn()
    entity_1.append(Name("Bob"))
    entity_1.append(Greeted())
    # Since entity_2 doesn't have a `Greeted` component it shouldn't be greeted by the system
    entity_2 = world.spawn()
    entity_2.append(Name("Mary"))

# The system that greets every component with a name
def hello_world(world: World): 
    # Query the entities with a name component and access its name component
    # (Since `Greeted` doesn't contain any data we can just ignore it by naming the reference `_`)
    for [entity, name, _] in world.query(Entity, Name, Greeted):
        print(f"Hello, {name.value}:{entity.id()}!")

# Create the app
app = App()
# Add the systems
app.add_startup_system(setup)
app.add_system(hello_world)
# Run the app
app.run()