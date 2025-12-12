import pygame
import sys
from state import *


pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.SCALED)
display = pygame.Surface((orig_size[0], orig_size[1]))
pygame.display.set_caption("Bloom and Brew")

stateManager.everythingState = EverythingState()
stateManager.push(WaitingRoomState())


GameData.gardenData["garden 1"]["plots"][0] = GardenPlant("plant1", 300)
GameData.gardenData["garden 1"]["plots"][1] = GardenPlant("plant2", 600)
GameData.gardenData["garden 2"]["plots"][0] = GardenPlant("sapling", 400)

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
                pygame.display.toggle_fullscreen()

    is_fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN


    stateManager.run(display, events)
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0,0))
    pygame.display.flip()
    delta = fpsClock.tick(30)/1000