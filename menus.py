import pygame

title = [
    " _   _   _   _   _____   _   _____   _     ____   __    ",
    "| | | | | \ | | |_   _| | | |_   _| | |   |  __| | . \  ",
    "| | | | |  \| |   | |   | |   | |   | |   | |_   | |\ \ ",
    "| | | | | \ ` |   | |   | |   | |   | |   |  _|  | || |",
    "| |_| | | |\  |   | |   | |   | |   | |__ | |__  | |/ / ",
    "\_____/ |_| \_|   |_|   |_|   |_|   |____||____| |__ /  "
]

pause_menu = [
    "+-------------------------+ ",
    "|                         |",
    "|       Game Paused       |",# Game Paused
    "|       ~~~~~~~~~~~       |",# ~~~~~~~~~~~
    "|                         |",
    "|                         |",
    "|                         |",
    "|                         |",
    "|                         |",# Continue
    "|                         |",
    "|                         |",
    "|                         |",# Restart
    "|                         |",
    "|                         |",
    "|                         |",# Save and quit
    "|                         |",
    "|                         |",
    "|                         |",
    "|                         |",
    "+-------------------------+",
]

hotbar = [
]

def render_main_menu(screen, font):
    for y, row in enumerate(title):
        for x, char in enumerate(row):
            if(char == " "):
                continue
            char = font.render(char, False, "White")
            screen.blit(char, (x * 16, y * 16))

def render_pause_menu(screen, font):
    width, height = pygame.display.get_surface().get_size()
    x_offset = width // 32 - len(pause_menu[0]) // 2
    y_offset = height // 32 - len(pause_menu) // 2
    pause_background = pygame.Surface((len(pause_menu[0]) * 16 - 16, len(pause_menu) * 16))
    pause_background.fill("Black")
    screen.blit(pause_background, (x_offset * 16, y_offset * 16))
    for y, row in enumerate(pause_menu):
        for x, char in enumerate(row):
            char = font.render(char, False, "White")
            screen.blit(char, (x * 16 + x_offset * 16, y * 16 + y_offset * 16))

