import pygame

def main_menu():
    global play_button, options_button, DISPLAY
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