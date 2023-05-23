import time, os, json
from pynput import keyboard
from map import Map
from clouds import Clouds
from Helicopter import Helicopter as Helico


MAP_W, MAP_H = 20, 20
TICK_SLEEP = 0.05
TREE_UP = 15
FIRE_UPDATE = 40
CLOUDS_UPDATE = 15

tick = 1
clouds = Clouds(MAP_W, MAP_H)
field = Map(MAP_W, MAP_H)
helico = Helico(MAP_W, MAP_H)
  
MOVES = {"w": (-1, 0), "d": (0, 1), "s": (1, 0), "a": (0, -1)}
def process_key(key):
    global helico, tick, clouds, field
    try:
        c = key.char.lower()
        if c in MOVES.keys():
            dx, dy = MOVES[c][0], MOVES[c][1]
            helico.move(dx, dy)
        if c == 'f':
            data = {"helicopter": helico.export_data(), 
                    "clouds": clouds.export_data(), 
                    "field": field.export_data(),
                    "tick": tick}
            with open("level.json", "w") as lvl:
                json.dump(data, lvl)
        if c == 'g':
            with open("level.json", "r") as lvl:
                data = json.load(lvl)
                tick = data["tick"] or 1
                field.import_data(data["field"])
                clouds.import_data(data["clouds"])
                helico.import_data(data["helicopter"])
    except AttributeError:
        print("WRONG KEY!!!")

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key,)
listener.start()

while True:
    os.system("cls")
    print("TICK", tick)
    field.process_helicopter(helico, clouds)
    helico.print_stats()
    field.print_map(helico, clouds)
    tick += 1
    time.sleep(TICK_SLEEP)
    if tick == 5:
        field.add_fire()
    if tick % TREE_UP == 0:
        field.grow_up_tree()
    if tick % FIRE_UPDATE == 0:
        field.update_fires(helico)
    if tick % CLOUDS_UPDATE == 0:
        clouds.update()