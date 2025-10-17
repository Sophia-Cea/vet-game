from utils import *

class Book:
    def __init__(self):
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/mainroom/book.png"), .3)
        self.rect = pygame.Rect(600,900,150,80)

    def render(self, screen):
        screen.blit(self.image, (400,600))

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        rect = self.rect
        clicked = rect.collidepoint(pos[0], pos[1])
        return clicked

class Arrow:
    def __init__(self, isLeft):
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/arrow.png"), .3)
        self.hoverImage = pygame.transform.smoothscale_by(pygame.image.load("images/ui/arrowGlowing.png"), .3)
        if not isLeft:
            self.pos = (1500, 400)
            self.image = pygame.transform.flip(self.image, True, False)
        if isLeft:
            self.pos = (20,400)
            self.hoverImage = pygame.transform.flip(self.hoverImage, True, False)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

    def render(self, screen):
        if self.checkClick():
            screen.blit(self.hoverImage, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        rect = self.rect
        clicked = rect.collidepoint(pos[0], pos[1])
        return clicked
    

class Coins:
    def __init__(self):
        self.copper = pygame.transform.smoothscale_by(pygame.image.load("images/ui/copper.png"), .1)
        self.silver = pygame.transform.smoothscale_by(pygame.image.load("images/ui/silver.png"), .1)
        self.gold = pygame.transform.smoothscale_by(pygame.image.load("images/ui/gold.png"), .1)
        self.textcol = (67, 40, 24)
    
    def render(self, screen):
        screen.blit(self.gold, (20,20))
        screen.blit(self.silver, (20,65))
        screen.blit(self.copper, (20,110))
        textRenderer.render(screen, str(GameData.gold), (70,30), 25, self.textcol)
        textRenderer.render(screen, str(GameData.silver), (70,75), 25, self.textcol)
        textRenderer.render(screen, str(GameData.copper), (70,120), 25, self.textcol)



class Animation:
    def __init__(self, path, imageNames, totalDuration, scale=1, flip=False):
        self.images = []
        for img in imageNames:
            self.images.append(pygame.transform.smoothscale_by(pygame.image.load(path+img), scale))
        
        if flip:
            for i, img in enumerate(self.images):
                self.images[i] = pygame.transform.flip(img, True, False)
        self.duration = totalDuration * 1000
        self.ticksPerFrame = self.duration//len(self.images)
        self.start_time = None
        self.currentFrame = 0

    def render(self, screen, pos):
        screen.blit(self.images[self.currentFrame], pos)

    def update(self):
        if self.start_time == None:
            self.start_time = pygame.time.get_ticks()
        self.currentTime = pygame.time.get_ticks()
        if (self.currentTime - self.start_time) >= self.ticksPerFrame:
            self.currentFrame += 1
            self.currentFrame %= len(self.images)
            self.start_time = pygame.time.get_ticks()


                
class MapButton:
    def __init__(self, isClosed):
        if isClosed:
            self.mapIcon = pygame.transform.smoothscale_by(pygame.image.load("images/ui/scroll.png"), .5)
        else: 
            self.mapIcon = pygame.transform.smoothscale_by(pygame.image.load("images/ui/map.png"), .5)
        self.rect = pygame.Rect(1400,30,150,150)

    def render(self, screen):
        screen.blit(self.mapIcon, (1400, 30))

    def update(self):
        if self.checkClick():
            pass

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        clicked = self.rect.collidepoint(pos[0], pos[1])
        return clicked