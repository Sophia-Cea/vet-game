import pygame
import sys
from state import *

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
pygame.mouse.set_visible(False)



# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# is_fullscreen = False

# def toggle_fullscreen():
#     global screen, is_fullscreen

#     is_fullscreen = not is_fullscreen

#     if is_fullscreen:
#         screen = pygame.display.set_mode(
#             (WIDTH, HEIGHT),
#             pygame.FULLSCREEN | pygame.SCALED
#         )
#     else:
#         screen = pygame.display.set_mode((WIDTH, HEIGHT))




cursor_size = (80, 80)
idle_cursor = pygame.image.load("images/ui/cursor/cursor_idle.png").convert_alpha()
click_cursor = pygame.image.load("images/ui/cursor/cursor_click.png").convert_alpha()
hover_cursor = pygame.image.load("images/ui/cursor/cursor_hover.png").convert_alpha()
idle_cursor = pygame.transform.scale(idle_cursor, cursor_size)
click_cursor = pygame.transform.scale(click_cursor, cursor_size)
hover_cursor = pygame.transform.scale(hover_cursor, cursor_size)

click_sound = pygame.mixer.Sound('audio/Cursor - 1.ogg')

offset_x = -50  
offset_y = -15 

pygame.mixer.init()
pygame.mixer.music.load("audio/Cozy Audio Background.wav")
pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1)

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
display = pygame.Surface((orig_size[0], orig_size[1]))
pygame.display.set_caption("Bloom and Brew")

stateManager.everythingState = EverythingState()
stateManager.push(WaitingRoomState()) 


GameData.gardenData["garden 1"]["plots"][0]["plant"] = GardenPlant("plant1", 300)
GameData.gardenData["garden 1"]["plots"][1]["plant"] = GardenPlant("plant2", 600)
GameData.gardenData["garden 1"]["plots"][2]["plant"] = GardenPlant("sapling", 900)

GameData.gardenData["garden 2"]["plots"][0]["plant"] = GardenPlant("sapling", 300)
GameData.gardenData["garden 2"]["plots"][1]["plant"] = GardenPlant("plant1", 600)
# GameData.gardenData["garden 2"]["plots"][2]["plant"] = GardenPlant("sapling", 900)


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # pygame.display.toggle_fullscreen()
                pass
            if event.key == pygame.K_TAB:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 is Left Click
                click_sound.play()

    is_fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN

    stateManager.run(display, events)

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    hover_rects = []
    if hasattr(stateManager.queue[-1], "get_hover_rects"):
        hover_rects = stateManager.queue[-1].get_hover_rects()

    hovering = any(rect.collidepoint(mouse_x, mouse_y) for rect in hover_rects)

    if mouse_pressed:
        current_cursor = click_cursor
    elif hovering:
        current_cursor = hover_cursor
    else:
        current_cursor = idle_cursor

    screen.blit(current_cursor, (mouse_x + offset_x, mouse_y + offset_y))

    pygame.display.flip()
    delta = fpsClock.tick(30) / 1000

