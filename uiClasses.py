from patient import *


class Arrow:
    def __init__(self, isLeft, pos):
        self.image = pygame.transform.scale_by(pygame.image.load("images/ui/arrow.png"), .2)
        if not isLeft:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        rect = self.rect
        clicked = rect.collidepoint(pos[0], pos[1])
        return clicked
    



    class Animation:
        def __init__(self, path, imageNames, totalDuration):
            self.images = []
            for img in imageNames:
                self.images.append(pygame.transform.scale_by(pygame.image.load(path+img), 1))
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
            self.mapIcon = pygame.transform.scale_by(pygame.image.load("images/ui/scroll.png"), .5)
        else: 
            self.mapIcon = pygame.transform.scale_by(pygame.image.load("images/ui/map.png"), .5)
        self.rect = pygame.Rect(1400,30,150,150)

    def render(self, screen):
        screen.blit(self.mapIcon, (1400, 30))

    def update(self):
        pass

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        clicked = self.rect.collidepoint(pos[0], pos[1])
        return clicked