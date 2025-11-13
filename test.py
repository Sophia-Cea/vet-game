import pygame
import sys


pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([1000, 700], pygame.SCALED)

points = [(200,225),(250,150),(250,200), (350,200), (350,250), (250,250),(250,300)]
rects = [pygame.Rect(250,200, 100,50), pygame.Rect(240,165,13,125), pygame.Rect(225,183,17,83), pygame.Rect(215,195, 17,60), pygame.Rect(200,215, 17,20)]

def render(screen):
    screen.fill((195,195,195))
    pygame.draw.polygon(screen, (0,0,200), points)
    for rect in rects:
        pygame.draw.rect(screen, (255,0,0), rect, 2)

def update():
    global rect
    pos = pygame.mouse.get_pos()
    rect = pygame.Rect(pos[0],pos[1], 1,1)

def handleInput(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidelistall(rects):
                print("true")

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    render(screen)
    update()
    handleInput(events)
    
    pygame.display.flip()
    delta = fpsClock.tick(30)/1000