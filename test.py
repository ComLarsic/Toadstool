from dataclasses import dataclass
from toadstool import App, Plugin, World
from toadstool.world import Entity, GameOver, Event

@dataclass
class TestComponent:
    bar: int

@dataclass
class TestEvent(Event):
    data: int

class TestPlugin(Plugin):
    def build(self, app: App):
        app.add_startup_system(setup)
        app.add_startup_system(test_component_queries)
        app.add_event_system(TestEvent, test_event)

def setup(world: World):
    a = world.spawn()
    a.append(TestComponent(0))
    b = world.spawn()
    b.append(TestComponent(32))
    c = world.spawn()
    c.append(TestComponent(20))

def test_component_queries(world: World):
    # Test quering components
    for [test] in world.query(TestComponent):
        print(f"-- TestComponent {test.bar} queried.")
    for [entity] in world.query(Entity):
        print(f"-- Entity {entity.id()} queried.")
    # Test double-querying
    for [a] in world.query(Entity):
        for [b] in world.query(Entity):
            print(f"-- Fetched {a.id()} and {b.id()}")

    world.dispatch_event(TestEvent(42))
    world.dispatch_event(TestEvent(20))
    world.dispatch_event(TestEvent(72))

def test_event(event: TestEvent, world: World):
    print(f"Recieved test_event with data {event.data}")
    world.insert_resource(GameOver())

def main():
    app = App()
    app.add_plugin(TestPlugin())
    app.run()

if __name__ == '__main__':
    main()