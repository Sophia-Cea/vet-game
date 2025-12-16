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


class VerticalArrow(UIthingy):
    def __init__(self, isDown):
        super().__init__()
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/down_arrow.png"), .3)
        self.hoverImage = pygame.transform.smoothscale_by(pygame.image.load("images/ui/down_arrow_hover.png"), .3)
        if not isDown:
            self.pos = (755, 5)
            self.image = pygame.transform.flip(self.image, False, True)
            self.hoverImage = pygame.transform.flip(self.hoverImage, False, True)
        if isDown:
            self.pos = (755, 830)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

    def render(self, screen):
        if self.checkClick():
            screen.blit(self.hoverImage, self.pos)
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
    def __init__(self):
        super().__init__()
        self.isClosed = True
        self.imageBig = pygame.transform.smoothscale_by(pygame.image.load("images/ui/scroll.png"), .43)
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/scroll.png"), .4)
        self.imageOpen = pygame.transform.smoothscale_by(pygame.image.load("images/ui/map.png"), .4)
        self.rect = pygame.Rect(1500,20,80,100)
        self.pos = [1480,10]
    
    def render(self, screen):
        pos = pygame.mouse.get_pos()
        if self.isClosed:
            if self.rect.collidepoint(pos):
                screen.blit(self.imageBig, [self.pos[0]-3, self.pos[1]-3])
            else:
                screen.blit(self.image, self.pos)
        else:
            screen.blit(self.imageOpen, self.pos)




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
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/garden/inventory-bag-closed.png"), 0.11)
        self.imageOpen = pygame.transform.smoothscale_by(pygame.image.load("images/garden/inventory-bag-open.png"), 0.11)
        self.imageBig = pygame.transform.smoothscale_by(pygame.image.load("images/garden/inventory-bag-closed.png"), 0.115)
        self.pos = (1490, 90)
        self.closed = True
        self.rect = pygame.Rect(1500, 132, 87, 75)

    def render(self, screen):
        pos = pygame.mouse.get_pos()
        hovering = self.rect.collidepoint(pos)

        if not self.closed:
            screen.blit(self.imageOpen, self.pos)
        else:
            if not hovering:
                screen.blit(self.image, self.pos)
            else:
                screen.blit(self.imageBig, [self.pos[0]-3, self.pos[1]-3])

        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        






class MedicalRoomInventoryButton(InventoryButton):
    def __init__(self):
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/MedicalRoomShelfButton.png").convert_alpha(), .4)
        self.hoverImage = pygame.transform.smoothscale_by(pygame.image.load("images/ui/MedicalRoomShelfClickWHITEBACK.png").convert_alpha(), .4)
        self.pos = (80, 150)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.hoverPos = [80,150]
        self.hoverPos[0] = self.hoverPos[0] - (self.hoverImage.get_width()-self.rect.w)/2
        self.hoverPos[1] = self.hoverPos[1] - (self.hoverImage.get_height()-self.rect.h)/2

    def render(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hoverImage, self.hoverPos)
        screen.blit(self.image, self.pos)



class ItemInInventory(UIthingy):
    def __init__(self, object, pos):
        super().__init__()
        self.pos = [pos[0], pos[1]]
        self.object = object
        self.quantity = object["quantity"]
        self.rectOriginal = pygame.Rect(self.pos[0]+5, self.pos[1]+10, 95,95)
        self.rect = pygame.Rect(self.pos[0]+5, self.pos[1]+10, 95,95)
        self.pos = [pos[0]-455, pos[1]-170]
        self.textOffset = [60,60]

    def render(self, screen, offset):
        screen.blit(self.image, (self.pos[0], self.pos[1]-offset))
        textRenderer.render(screen, str(self.quantity), (self.pos[0]+self.textOffset[0], self.pos[1]+self.textOffset[1]-offset), 35, (255,255,255))
        self.rect.y = self.rectOriginal.y - offset

    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)


class PotionItemInInventory(ItemInInventory):
    def __init__(self, potionObject, pos):
        super().__init__(potionObject, pos)
        self.data = potionInfo["potions"][self.object["name"]]
        self.image = pygame.transform.scale_by(pygame.image.load("images/potionRoom/potionBottles/" + self.data["image"]), 6)
        # self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())
        self.pos[0] += 25
        self.pos[1] += 25
        self.textOffset = [45,40]



class SeedItemInInventory(ItemInInventory):
    def __init__(self, seedObject, pos):
        super().__init__(seedObject, pos)
        self.data = plantInfo[seedObject["name"]]
        self.image = pygame.transform.smoothscale_by(pygame.image.load(self.data["path"] + "seed-bag.png"), .055)
        self.textOffset = [55,45]
        self.pos[0] += 15
        self.pos[1] += 20
        # self.rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())



class InventoryStateRoundButton:
    def __init__(self, image, center, radius):
        self.imageBig = image
        self.image = pygame.transform.smoothscale_by(self.imageBig, 0.93)
        self.center = center
        self.radius = radius
        self.isBig = False

    def render(self, screen):
        if not self.isBig:
            screen.blit(self.image, (self.center[0]-self.radius-15, self.center[1]-self.radius-5))
        else:
            screen.blit(self.imageBig, (self.center[0]-self.radius-20, self.center[1]-self.radius-10))
        # pygame.draw.circle(screen, (255,0,0), self.center, self.radius, 2)

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        dist = math.sqrt((pos[1]-self.center[1])**2 + (pos[0]-self.center[0])**2)
        if dist <= self.radius:
            return True
        return False


class RelocatePopup(UIthingy):
    def __init__(self, patient):
        super().__init__()
        self.patient = patient
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_.png"), .35)
        self.pos = [500,100]
        self.rect = pygame.Rect(510,115,580,510)
        self.roomButton = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_popup_button.png"), .35)
        self.uibutton = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_popup_button2.png"), .35)
        self.selectedButton = None

        self.sendToRoomRect = pygame.Rect(630, 575, 140, 40)
        self.cancelRect = pygame.Rect(840, 575, 140, 40)
        self.sentToRoom = False

    def render(self, screen):
        super().render(screen)
        screen.blit(self.image, self.pos)
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        for i in range(8):
            x = 600 + (i%4)*105
            y = 340 + (i//4)*105
            screen.blit(self.roomButton, (x,y))
            textRenderer.render(screen, "Room", (x+53, y+35), 20, (40,20,10), align="center")
            textRenderer.render(screen, str(i+1), (x+53, y+65), 35, (40,20,10), align="center")
            if self.selectedButton != None:
                if self.selectedButton == i:
                    pygame.draw.circle(screen, (255,255,255), (x+52, y+51), 50, 5)
        
        textRenderer.render(screen, "Patient Check-In", (720, 170), 30, (40,20,10))
        textRenderer.render(screen, "Patient:", (700, 215), 20, (40,20,10))
        textRenderer.render(screen, "Illness:", (870, 215), 20, (40,20,10))

        textRenderer.render(screen, "Paige", (790, 215), 20, (40,20,10))
        textRenderer.render(screen, self.patient.illness, (960, 215), 20, (40,20,10))

        if self.selectedButton != None:
            screen.blit(self.uibutton, (310, 100))
            textRenderer.render(screen, "Send to Room", (700, 595), 15, (40,20,10), align="center")

        screen.blit(self.uibutton, (520, 100))
        textRenderer.render(screen, "Cancel", (910, 595), 15, (40,20,10), align="center")

        pos = pygame.mouse.get_pos()
        if self.sendToRoomRect.collidepoint(pos) and self.selectedButton != None:
            pygame.draw.rect(screen, (255,255,255), self.sendToRoomRect, 5)
        if self.cancelRect.collidepoint(pos):
            pygame.draw.rect(screen, (255,255,255), self.cancelRect, 5)


    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(8):
                    x = 652 + (i%4)*105
                    y = 351 + (i//4)*105
                    r = 45
                    if math.sqrt((pos[0]-x)**2 + (pos[1]-y)**2) <= r:
                        self.selectedButton = i
                if self.selectedButton != None and self.sendToRoomRect.collidepoint(pos):
                    GameData.patientsInRooms[self.selectedButton] = self.patient
                    GameData.activePatients.remove(self.patient)
                    self.sentToRoom = True




class ScrollBar:
    def __init__(self, outsideRect, insideRect, outsideColor, insideColor):
        self.insideRect = insideRect
        self.outsideRect = outsideRect
        self.scrollBarRange = [self.outsideRect.y+3, self.outsideRect.y+self.outsideRect.h-self.insideRect.h]
        self.outsideColor = outsideColor
        self.insideColor = insideColor
        self.draggingBar = False
        self.draggingBarOffset = 0
        self.offset = 0

    def render(self, screen):
        pygame.draw.rect(screen, self.insideColor, self.insideRect, border_radius=10)
        pygame.draw.rect(screen, self.outsideColor, self.outsideRect, 6, 10)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.draggingBar:
            self.insideRect.y = pos[1] - self.draggingBarOffset
            if self.insideRect.y < self.scrollBarRange[0]:
                self.insideRect.y = self.scrollBarRange[0]
            if self.insideRect.y > self.scrollBarRange[1]:
                self.insideRect.y = self.scrollBarRange[1]

        self.offset = self.insideRect.y - self.scrollBarRange[0]

    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.insideRect.collidepoint(pos):
                    self.draggingBar = True
                    self.draggingBarOffset = pos[1] - self.insideRect.y
            if event.type == pygame.MOUSEBUTTONUP:
                self.draggingBar = False