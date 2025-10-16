from uiClasses import *

class StateManager:
    def __init__(self) -> None:
        self.queue = []
        self.transitioning = False
        bg1pos = 0
        bg2pos = -WIDTH

    def push(self, page):
        self.transitioning = True
        self.queue.append(page)
        page.onEnter()

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)

    def run(self, surface, events):
        if not self.transitioning:
            self.queue[len(self.queue)-1].update()
            if len(self.queue) > 1:
                self.queue[len(self.queue)-2].render(surface)
            self.queue[len(self.queue)-1].render(surface)
            self.queue[len(self.queue)-1].handleInput(events)
        else:
            self.transitioning = False




class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass

stateManager = StateManager()

class PatientRoomState(State):
    def __init__(self) -> None:
        super().__init__()
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/backgroundmain.png"), (orig_size[0], orig_size[1]))
        self.desk = pygame.transform.scale_by(pygame.image.load("images/mainroom/desk.png"), .4)
        pygame.draw.rect(self.background, (125, 79, 80), (500,200,150, 250))
        self.patients = [EasyPatient()]
        self.leftArrow = Arrow(True, (20,200))
        self.rightArrow = Arrow(False, (1500, 200))
        self.mapIconClosed = MapButton(True)
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed]

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (0,0))
        for patient in self.patients:
            patient.render(screen)
        screen.blit(self.desk, (0, 0))
        for element in self.uiElements:
            element.render(screen)

    def update(self):
        super().update()
        for patient in self.patients:
            patient.update()

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.push(PotionRoomState())
                if self.rightArrow.checkClick():
                    stateManager.push(GardenState())
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())


class PotionRoomState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/potionroom.png"), (orig_size[0], orig_size[1]))
        self.cauldron = pygame.transform.scale_by(pygame.image.load("images/potionRoom/cauldronAnimation/cauldron.png"), .7)
        self.table = pygame.Surface((400,200))
        self.table.fill((64, 61, 57))
        self.leftArrow = Arrow(True, (20,200))
        self.rightArrow = Arrow(False, (1500, 200))
        self.mapIconClosed = MapButton(True)
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed]

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (0,0))
        # screen.blit(self.table, (450,380))
        screen.blit(self.cauldron, (645,340))
        for element in self.uiElements:
            element.render(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rightArrow.checkClick():
                    stateManager.pop()
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())



class GardenState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.Surface([orig_size[0], orig_size[1]])
        self.background.fill((182, 204, 254))
        pygame.draw.rect(self.background, (132, 169, 140), (0, 600, 1600, 500))
        self.leftArrow = Arrow(True, (20,200))
        self.rightArrow = Arrow(False, (1500, 200))
        self.mapIconClosed = MapButton(True)
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed]

    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (0,0))
        for element in self.uiElements:
            element.render(screen)


    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.pop()
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())



class MapState(State):
    def __init__(self):
        super().__init__()
        self.map = pygame.transform.scale_by(pygame.image.load("images/ui/mapui.png"), .6)
        self.rect = pygame.Rect(200,200,1000,600)
        self.darkbg = pygame.Surface(orig_size)
        self.darkbg.fill((0,0,0))
        self.darkbg.set_alpha(90)
        self.mapIcon = MapButton(False)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.darkbg, (0,0))
        screen.blit(self.map, (310,130))
        self.mapIcon.render(screen)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mapIcon.checkClick():
                    stateManager.pop()
    

