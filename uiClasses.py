from utils import *


class UIthingy:
    def __init__(self):
        self.pos = [0,0]
        self.rect = pygame.Rect(0,0,0,0)
        self.image = None
    
    def render(self, screen):
        screen.blit(self.image, self.pos)

    def update(self):
        pass

    def handleInput(self, events):
        pass

    def checkClick(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())





class Book(UIthingy):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/mainroom/book.png"), .3)
        self.rect = pygame.Rect(1000,650,150,80)
        self.pos = [1100,660]


class Arrow(UIthingy):
    def __init__(self, isLeft):
        super().__init__()
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
            screen.blit(self.hoverImage, self.pos)
        else:
            super().render(screen)


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

class SmallArrow(Arrow):
    def __init__(self, isLeft):
        super().__init__(isLeft)
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/ui/left_arrow.png"), .1)
        self.hoverImage = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/ui/left_arrow.png"), .1)
        self.pos = [60, 190]
        self.rect = pygame.Rect(self.pos[0]+13, self.pos[1]+00, 35,60)
        if not isLeft:
            self.image = pygame.transform.flip(self.image, True, False)
            self.hoverImage = pygame.transform.flip(self.hoverImage, True, False)
            self.pos = [1425, 190]
            self.rect = pygame.Rect(self.pos[0]+20, self.pos[1]+0, 35,60)

class XButton(UIthingy):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/x_button.png"), .06)
        self.hoverImg = pygame.transform.smoothscale_by(pygame.image.load("images/ui/x_highlight.png"), .06)
        self.pos = [pos[0], pos[1]]
        self.rect = pygame.Rect(pos[0], pos[1], 45,45)

    def render(self, screen):
        if self.checkClick():
            screen.blit(self.hoverImg, self.pos)
        super().render(screen)

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

         
class MapButton(UIthingy):
    def __init__(self, isClosed):
        super().__init__()
        if isClosed:
            self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/scroll.png"), .5)
        else: 
            self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/map.png"), .5)
        self.rect = pygame.Rect(1400,30,150,150)
        self.pos = [1400,30]



class BrewButton(UIthingy):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300,100))
        self.image.fill((200,0,100))
        self.pos = [620,600]
        self.rect = pygame.Rect(620,600,300,100)

    def render(self, screen):
        super().render(screen)
        textRenderer.render(self.image, "Brew", (150, 50), 35, (255,255,255), align="center")


class InventoryButton(UIthingy):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300,200))
        self.image.fill((100,100,80))
        self.pos = [40,800]
        self.rect = pygame.Rect(40,800,300,200)


class ItemInInventory(UIthingy):
    def __init__(self, object, pos):
        super().__init__()
        self.pos = [pos[0], pos[1]]
        self.object = object
        self.quantity = object["quantity"]

    def render(self, screen):
        super().render(screen)
        textRenderer.render(screen, str(self.quantity), (self.pos[0]+60, self.pos[1]+60), 35, (255,255,255))

    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)



class PotionItemInInventory(ItemInInventory):
    def __init__(self, potionObject, pos):
        super().__init__(potionObject, pos)
        self.data = potionInfo["potions"][self.object["name"]]
        self.image = pygame.transform.scale_by(pygame.image.load("images/potionRoom/potionBottles/" + self.data["image"]), 8)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())



    

class SeedItemInInventory(ItemInInventory):
    def __init__(self, seedObject, pos):
        super().__init__(seedObject, pos)
        self.data = plantInfo[seedObject["name"]]
        self.image = pygame.transform.smoothscale_by(pygame.image.load(self.data["path"] + "seed.png"), .25)
        self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

        
    