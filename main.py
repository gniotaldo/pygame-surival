import pygame
import random
from typing import List
from pygame.math import Vector2
from pygame.locals import *
from misc.config import *
from misc.images import bottomBarImg, pausedImg, pausedIcon, invBack
from classes.Map import Map
from classes.Agent import Agent
import math
import os
import pygame.locals as pl

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


SCREEN_WIDTH = WIDTH*TILE_SIZE
SCREEN_HEIGHT = HEIGHT*TILE_SIZE




def main_menu():
    global play_button, options_button
    # Wyświetlanie menu głównego
    DISPLAY.fill((0, 0, 0))  # Czarny ekran
    title_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render('Główne Menu', True, (255, 255, 255))
    play_button = pygame.Rect(100, 200, 200, 50)
    options_button = pygame.Rect(100, 300, 200, 50)

    pygame.draw.rect(DISPLAY, (255, 0, 0), play_button)
    pygame.draw.rect(DISPLAY, (0, 255, 0), options_button)

    DISPLAY.blit(title_text, (150, 100))
    play_text = font.render('Graj', True, (255, 255, 255))
    options_text = font.render('Ustawienia', True, (255, 255, 255))
    DISPLAY.blit(play_text, (play_button.x + 20, play_button.y + 15))
    DISPLAY.blit(options_text, (options_button.x + 20, options_button.y + 15))

def new_game_menu():
    global active_input, MAP_SIZE, RANDOMSEED, SEED, new_game_settings, newgame_button
    DISPLAY.fill((0, 0, 0))  # Czarny ekran
    title_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render('Nowa Gra', True, (255, 255, 255))
    DISPLAY.blit(title_text, (100, 50))
    
    y_offset = 150
    input_rects = {}
    
    for key, value in new_game_settings.items():
        label = font.render(key, True, (255, 255, 255))
        DISPLAY.blit(label, (100, y_offset))
        input_rect = pygame.Rect(300, y_offset, 200, 30)
        input_text = font.render(str(value), True, (255, 255, 255))  # Konwersja na string
        if active_input == key:
            pygame.draw.rect(DISPLAY, active_color, input_rect, 2)
        else:
            pygame.draw.rect(DISPLAY, text_color, input_rect, 2)
        DISPLAY.blit(input_text, (input_rect.x + 5, input_rect.y + 5))
        input_rects[key] = input_rect
        y_offset += 50

    new_game_button = pygame.Rect(100, y_offset, 200, 50)

    
    #graj
    newgame_button = pygame.Rect(100, 400, 200, 50)
    pygame.draw.rect(DISPLAY, (0, 0, 255), newgame_button)
    newgame_text = font.render('nowa gra', True, (255, 255, 255))
    DISPLAY.blit(newgame_text, (newgame_button.x + 20, newgame_button.y + 15))
    
    return input_rects, new_game_button



def get_setting_value(setting):
    if setting.endswith("_BT"):
        key_value: int = int(settings[setting])
        return get_key_name(key_value) if key_value is not None and not isinstance(key_value, str) else  key_value if isinstance(key_value, str) else "None"
    else:
        return str(settings[setting])

def apply_settings():
    with open("settings.txt", "w") as f:
        for key, value in settings.items():
            f.write(f"{key} = {value}\n")
    load_settings()
    
def settings_menu():
    global back_button, labels, inputs, save_button, active_input, apply_button


    # Czarny ekran
    DISPLAY.fill((0, 0, 0))

    # Etykieta tytułowa
    title_font = pygame.font.SysFont(None, 40)
    title_text = title_font.render('Menu Ustawień', True, (255, 255, 255))
    DISPLAY.blit(title_text, (50, 20))

    # Przycisk powrotu
    back_button = pygame.Rect(500, 100, 200, 50)
    pygame.draw.rect(DISPLAY, button_color, back_button)
    back_text = font.render('Powrót', True, text_color)
    DISPLAY.blit(back_text, (back_button.x + 20, back_button.y + 15))

    #ZASTOSUJ
    apply_button = pygame.Rect(10, 100, 200, 50)
    pygame.draw.rect(DISPLAY, (0, 0, 255), apply_button)
    apply_text = font.render('Zastosuj', True, (255, 255, 255))
    DISPLAY.blit(apply_text, (apply_button.x + 20, apply_button.y + 15))

    # Wyświetlanie etykiet i pól tekstowych
    for key, label in labels.items():
        DISPLAY.blit(label, (50, inputs[key].y + 10))
    for key, rect in inputs.items():
        input_text = font.render(get_setting_value(key), True, text_color)
        if active_input == key:
            pygame.draw.rect(DISPLAY, active_color, rect, 2)
        else:
            pygame.draw.rect(DISPLAY, input_color, rect, 2)
        DISPLAY.blit(input_text, (rect.x + 5, rect.y + 10))
        

    # Przycisk zapisu ustawień
    save_button = pygame.Rect(250, 100, 200, 50)
    pygame.draw.rect(DISPLAY, button_color, save_button)
    save_text = font.render("Zapisz Ustawienia", True, text_color)
    DISPLAY.blit(save_text, (save_button.x + 20, save_button.y + 15))


def render_screen():
    global in_mainMenu, in_settings, new_game_input_rects, new_game_button

    if in_mainMenu:
        main_menu()
    elif in_newGame:
        new_game_input_rects, new_game_button = new_game_menu()
    elif in_settings:
        settings_menu()



def draw_button(screen, text, rect, color, recipe):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))
    
    recipe_text = font.render(recipe, True, (255, 255, 255))
    screen.blit(recipe_text, (rect.x + rect.width + 10, rect.y + (rect.height - text_surface.get_height()) // 2))


# Lista przycisków
buttons = [
    {"text": "doors", "recipe": "6x Wood", "rect": pygame.Rect(350, 250, 200, 50), "color": RED, "function": Map.Item.ItemType.Doors},
    {"text": "furnace", "recipe": "8x Cobblestone", "rect": pygame.Rect(350, 350, 200, 50), "color": GREEN, "function": Map.Item.ItemType.Furnace},
    {"text": "glass", "recipe": "4x Grass", "rect": pygame.Rect(350, 450, 200, 50), "color": BLUE, "function": Map.Item.ItemType.Glass}
]

def displayBar():
    global inventory_counts, equipped_item_index, equipped_item, equipped_islast, HEIGHT, WIDTH
    

    inventory_counts.clear() 
    for item in agent.inventory:
        inventory_counts[item] = inventory_counts.get(item, 0) + 1
    if len(agent.inventory) == 0:
        equipped_item_index = None
        equipped_item = None
    elif len(set(agent.inventory)) == 1:
        equipped_item_index = 0
        equipped_item = list(inventory_counts)[equipped_item_index]

    elif agent.inventory != []:
        if not equiped_islast:
            equipped_item = list(inventory_counts)[equipped_item_index]
        else: 
            try:
                equipped_item = list(inventory_counts)[equipped_item_index]
            except IndexError:
                equipped_item_index -= 1
                equipped_item = list(inventory_counts)[equipped_item_index]

    DISPLAY.blit(bottomBarImg,(0, HEIGHT*TILE_SIZE))
    x_pos = 10
    y_pos = (HEIGHT+BOTTOMBAR/2) * TILE_SIZE - 5

    for item, count in inventory_counts.items():
        text_color = (255, 255, 255) 
        if equipped_item_index is not None and count > 0 and item == list(inventory_counts.keys())[equipped_item_index]:
            text_color = (255, 0, 0)
        text = font.render(f"{item}: {count}", True, text_color)
        DISPLAY.blit(text, (x_pos, y_pos))
        x_pos += text.get_width() + 10


    texthelper = font.render("COORDS: 444.44, 444.44", True, (255, 255, 255))
    maxwidth = texthelper.get_width()
    textCords = font.render(f"COORDS: {agent.position.x}, {agent.position.y}", True, (255, 255, 255))
    DISPLAY.blit(textCords, (WIDTH * TILE_SIZE - maxwidth - 10, y_pos))




def tick():
    CLOCK.tick(FRAMERATE)
    world_map.render(DISPLAY, renderLeft, renderTop)
    agent.render(DISPLAY, renderLeft, renderTop)
    displayBar()
    if showEq:
        DISPLAY.blit(invBack,(0,0))
        for button in buttons:
            draw_button(DISPLAY, button["text"], button["rect"], button["color"], button["recipe"])
    if paused:
        if ticks % 40 in range (0,30):
            DISPLAY.blit(pausedImg,(0, 0))
        DISPLAY.blit(pausedIcon,(0, 0))
        
        
    pygame.display.flip()
    pygame.display.update()

def updateCamera():
    rendLeft = agent.position.x - WIDTH/2
    rendTop = agent.position.y - HEIGHT/2
    if rendTop < 0:
        rendTop = 0
    if rendTop > (MAP_SIZE) * 20 - HEIGHT:
        rendTop = (MAP_SIZE) * 20 - HEIGHT
    if rendLeft < 0:
        rendLeft = 0
    if rendLeft > (MAP_SIZE) * 20 - WIDTH:
        rendLeft= (MAP_SIZE) * 20- WIDTH
    return rendLeft, rendTop

def bind_key(setting):
    # Oczekiwanie na wciśnięcie klawisza
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            return event.key

# Mapowanie identyfikatorów klawiszy na bardziej przyjazne nazwy
key_names = {
    pl.K_SPACE: "SPACE",
    pl.K_RETURN: "RETURN",
    pl.K_BACKSPACE: "BACKSPACE",
    # Tutaj możesz dodać inne mapowania
}

def get_key_name(key):
    return key_names.get(key, pygame.key.name(key))


def load_settings():
        global settings, SCREEN_WIDTH, SCREEN_HEIGHT, MUSICVOLUME, PAUSE_BT, SHOWEQ_BT, MOVEUP_BT, MOVEDOWN_BT, MOVELEFT_BT, MOVERIGHT_BT, DISPLAY, HEIGHT, WIDTH
        try:
            with open(settings_file, "r") as file:
                for line in file:
                    key, value = line.strip().split(" = ")
                    settings[key] = value
                SCREEN_WIDTH = int(settings["SCREEN_WIDTH"])
                SCREEN_HEIGHT = int(settings["SCREEN_HEIGHT"])
                MUSICVOLUME = float(settings["MUSICVOLUME"])
                PAUSE_BT = int(settings.get("PAUSE_BT")) 
                SHOWEQ_BT = int(settings.get("SHOWEQ_BT"))
                MOVEUP_BT = int(settings["MOVEUP_BT"])
                MOVEDOWN_BT = int(settings.get("MOVEDOWN_BT"))
                MOVELEFT_BT = int(settings.get("MOVELEFT_BT"))
                MOVERIGHT_BT = int(settings.get("MOVERIGHT_BT"))
                pygame.mixer.music.set_volume(MUSICVOLUME) 
                door_closed.set_volume(MUSICVOLUME)
                door_opened.set_volume(MUSICVOLUME)
                WIDTH = int((SCREEN_WIDTH - RIGHTBAR) / TILE_SIZE)
                SCREEN_WIDTH = (WIDTH + RIGHTBAR) * TILE_SIZE
                HEIGHT = int((SCREEN_HEIGHT - BOTTOMBAR) / TILE_SIZE)
                SCREEN_HEIGHT = (HEIGHT + BOTTOMBAR) * TILE_SIZE
                DISPLAY = pygame.display.set_mode(((WIDTH+RIGHTBAR) * TILE_SIZE, (HEIGHT+BOTTOMBAR) * TILE_SIZE))

        except FileNotFoundError:
            pass

def start_new_game():
    global MAP_SIZE, RANDOMSEED, SEED, SEALEVEL
    try:
        MAP_SIZE = int(new_game_settings["MAP_SIZE"])
    except ValueError:
        MAP_SIZE = 10  # Domyślna wartość lub odpowiednie przetwarzanie błędu

    RANDOMSEED = new_game_settings["RANDOMSEED"].lower() in ("true", "1")

    try:
        SEED = int(new_game_settings["SEED"])
    except ValueError:
        SEED = 20
    try:
        SEALEVEL = int(new_game_settings["SEALEVEL"])
    except ValueError:
        SEALEVEL = 0

if __name__ == '__main__': 
    global active_input
    in_mainMenu = True
    startGame = False
    in_settings = False
    in_newGame = False
    in_game = False
    running = True
    pygame.init()
    DISPLAY = pygame.display.set_mode(((WIDTH+RIGHTBAR) * TILE_SIZE, (HEIGHT+BOTTOMBAR) * TILE_SIZE))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption('gierka')
    font = pygame.font.SysFont(None, 25, True, True)
    text_color = pygame.Color('white')
    input_color = pygame.Color('gray12')
    active_color = pygame.Color('dodgerblue2')
    button_color = pygame.Color('limegreen')

    # Teksty etykiet
    labels = {
        "SCREEN_WIDTH": font.render("Screen width:", True, text_color),
        "SCREEN_HEIGHT": font.render("Screen height:", True, text_color),
        "MUSICVOLUME": font.render("Music volume:", True, text_color),
        "PAUSE_BT": font.render("Pause:", True, text_color),
        "SHOWEQ_BT": font.render("Inventory:", True, text_color),
        "MOVEUP_BT": font.render("Move up:", True, text_color),
        "MOVEDOWN_BT": font.render("Move fown:", True, text_color),
        "MOVELEFT_BT": font.render("Move left:", True, text_color),
        "MOVERIGHT_BT": font.render("Move right:", True, text_color),
    }

    settings = {
    "SCREEN_WIDTH": str(SCREEN_WIDTH),
    "SCREEN_HEIGHT": str(SCREEN_HEIGHT),
    "MUSICVOLUME": str(0.1),
    "PAUSE_BT": pygame.K_SPACE,
    "SHOWEQ_BT": pygame.K_q,
    "MOVEUP_BT": pygame.K_w,
    "MOVEDOWN_BT": pygame.K_s,
    "MOVELEFT_BT": pygame.K_a,
    "MOVERIGHT_BT": pygame.K_d,
    }

    
    new_game_settings = {
        "MAP_SIZE": str(MAP_SIZE),
        "RANDOMSEED": str(int(RANDOMSEED)),
        "SEED": str(SEED),
        "SEALEVEL": str(SEALEVEL)
    }
    print(settings)
    print(new_game_settings)

    settings_file = "settings.txt"

    



    # Pola tekstowe
    inputs = {key: pygame.Rect(300, 50 * i + 200, 200, 40) for i, key in enumerate(settings.keys())}
    active_input = None

    # Przycisk do zapisu ustawień
    save_button = pygame.Rect(300, 500, 200, 50)

    pygame.mixer.music.load('sounds/background.mp3')
    door_opened = pygame.mixer.Sound('sounds/dooropen.wav')
    door_closed = pygame.mixer.Sound('sounds/doorclosed.wav')
    
    door_closed.set_volume(MUSICVOLUME)
    door_opened.set_volume(MUSICVOLUME)
    pygame.mixer.music.set_volume(MUSICVOLUME) 
    pygame.mixer.music.play(-1)
    os.system('cls')

    
    load_settings()

    while not in_game and not startGame and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if in_settings:  # Lewy przycisk myszy
                        for key, rect in inputs.items():
                            if rect.collidepoint(event.pos):
                                active_input = key
                            if active_input and active_input.endswith("_BT"):
                                settings_menu()
                                pygame.display.flip()
                                settings[active_input] = bind_key(active_input)
                                active_input = None
                            if save_button.collidepoint(event.pos):
                                # Zapisanie ustawień
                                with open("settings.txt", "w") as f:
                                    for key, value in settings.items():
                                        f.write(f"{key} = {value}\n")
                            elif apply_button.collidepoint(event.pos):
                                apply_settings()
                    if in_newGame:
                        for key, rect in new_game_input_rects.items():
                            print(new_game_settings)
                    
                            if rect.collidepoint(event.pos):
                                active_input = key
                                if active_input == "RANDOMSEED":
                                    new_game_settings[active_input] = "False" if new_game_settings[active_input] == "True" else "True"
                                break
                        else:
                            active_input = None
                if in_mainMenu:
                    mouse_pos = event.pos
                    if play_button.collidepoint(mouse_pos):
                        in_newGame = True
                        in_mainMenu = False
                    elif options_button.collidepoint(mouse_pos):
                        in_settings = True
                        in_mainMenu = False
                elif in_settings:
                    mouse_pos = event.pos
                    if back_button.collidepoint(mouse_pos):
                        in_settings = False
                        in_mainMenu = True
                elif in_newGame:
                    if newgame_button.collidepoint(event.pos):
                        start_new_game()
                        startGame = True
                        in_newGame = False
                        in_mainMenu = False
                    #elif back_button.collidepoint(mouse_pos):
                    #    in_newGame = False
                    #    in_mainMenu = True
            elif event.type == pygame.KEYDOWN:
                if in_settings and active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        settings[active_input] = settings[active_input][:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            float_value = float(settings[active_input])
                            settings[active_input] = float_value
                        except ValueError:
                            pass
                        active_input = None
                    else:
                        settings[active_input] += event.unicode
                if active_input is not None and in_newGame:
                
                    if active_input == "RANDOMSEED":
                        if event.key == pygame.K_RETURN:
                            new_game_settings[active_input] = "False" if new_game_settings[active_input] == "True" else "True"
                    elif event.key == pygame.K_BACKSPACE:
                        new_game_settings[active_input] = new_game_settings[active_input][:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            float_value = float(new_game_settings[active_input])
                            new_game_settings[active_input] = float_value
                        except ValueError:
                            pass
                        active_input = None
                    else:
                        new_game_settings[active_input] += event.unicode
        render_screen()
        pygame.display.flip()
        if startGame:
            in_mainMenu = False
            is_running = True
    if is_running:
        
        world_map = Map(20*MAP_SIZE, 20*MAP_SIZE, TILE_SIZE, RANDOMSEED, SEED, MAP_SIZE, SEALEVEL)
        agent = Agent(TILE_SIZE,world_map)
        paused = False
        showEq = False
        ticks = 0
        equipped_item_index = None
        equiped_islast = True
        inventory_counts = {}

    while is_running:
        renderLeft, renderTop = updateCamera()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == KEYDOWN:
                if event.key == PAUSE_BT:
                    paused = not paused
                    ticks = 0
                    if paused:
                        pygame.mixer.music.pause()  # Pauza muzyki
                    else:
                        pygame.mixer.music.unpause()  # Wznowienie muzyki
                elif not paused:
                    if event.key == SHOWEQ_BT:
                        showEq = not showEq
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:

                if showEq:
                    mouse_pos = event.pos
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            agent.craft(button['function'])
                
                #LMB
                elif event.button == 1:
                    clicked_x = int(math.floor(event.pos[0]/TILE_SIZE + renderLeft))
                    clicked_y = int(math.floor(event.pos[1]/TILE_SIZE + renderTop))
                    agent.destroy(clicked_x, clicked_y)

                elif event.button == 2:
                    clicked_x = int(math.floor(event.pos[0]/TILE_SIZE + renderLeft))
                    clicked_y = int(math.floor(event.pos[1]/TILE_SIZE + renderTop))
                    pole = world_map.map_grid[clicked_x][clicked_y].type
                    print(f"typ pola: {pole}")

                #RMB
                elif event.button == 3:
                    clicked_x = int(math.floor(event.pos[0]/TILE_SIZE + renderLeft))
                    clicked_y = int(math.floor(event.pos[1]/TILE_SIZE + renderTop))
                    if world_map.map_grid[clicked_x][clicked_y].type == Map.Item.ItemType.Doors:
                        world_map.map_grid[clicked_x][clicked_y].type = Map.Item.ItemType.OpenDoors
                        door_opened.play()
                    elif world_map.map_grid[clicked_x][clicked_y].type == Map.Item.ItemType.OpenDoors:
                        world_map.map_grid[clicked_x][clicked_y].type = Map.Item.ItemType.Doors
                        door_closed.play()
                    elif world_map.map_grid[clicked_x][clicked_y].type == Map.Item.ItemType.Furnace:
                        #showFurnace = True
                        ...
                    else:
                        agent.place(equipped_item, clicked_x, clicked_y)


                elif event.button == 4:
                    if equipped_item_index is not None:
                        if equipped_item_index < len(set(agent.inventory)) - 1:
                            equipped_item_index += 1
                            equipped_item = list(inventory_counts)[equipped_item_index]

                elif event.button == 5:
                    if equipped_item_index is not None:
                        if equipped_item_index != 0:
                            equipped_item_index -= 1
                            equipped_item = list(inventory_counts)[equipped_item_index]

                           
        if not showEq and not paused:
            keys = pygame.key.get_pressed()
            if keys[MOVEUP_BT]:
                agent.move('W', world_map)
            if keys[MOVEDOWN_BT]:
                agent.move('S', world_map)
            if keys[MOVELEFT_BT]:
                agent.move('A', world_map)
            if keys[MOVERIGHT_BT]:
                agent.move('D', world_map)

        tick()
        ticks += 1
    pygame.quit()
