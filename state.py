from otherClasses import *

class StateManager:
    def __init__(self) -> None:
        self.queue = []
        self.transitioning = False
        self.transitioningLeft = None
        self.bgOldOffset = [0,0]
        self.bgNewOffset = [0,0]
        self.everythingState = None

    def push(self, page):
        self.queue.append(page)
        page.onEnter()

    def transition(self, transitioningLeft):
        self.transitioning = True
        self.transitioningLeft = transitioningLeft
        if self.transitioningLeft:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [-WIDTH,0]
        else:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [WIDTH,0]

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)
        

    def run(self, surface, events):
        self.everythingState.render(surface, [0,0])
        self.everythingState.update()
        self.everythingState.handleInput(events)
        if not self.transitioning:
            self.queue[len(self.queue)-1].update()
            if len(self.queue) > 1:
                self.queue[len(self.queue)-2].render(surface, [0,0])
            self.queue[len(self.queue)-1].render(surface, [0,0])
            self.queue[len(self.queue)-1].handleInput(events)
        else:
            self.queue[len(self.queue)-1].render(surface, self.bgNewOffset)
            self.queue[len(self.queue)-2].render(surface, self.bgOldOffset)
            self.queue[len(self.queue)-1].update()
            self.queue[len(self.queue)-2].update()
            movement = (self.bgNewOffset[0])/6
            self.bgNewOffset[0] -= movement
            self.bgOldOffset[0] -= movement
            if self.bgNewOffset[0] > -3 and self.bgNewOffset[0] < 3:
                self.transitioning = False
                self.queue.remove(self.queue[-2])

class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen, offset):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass

stateManager = StateManager()

class EverythingState(State):
    def __init__(self):
        super().__init__()
        self.currentTime = pygame.time.get_ticks()
        self.interval = 100
        self.animalList = sum_animal_values(GameData.animalData)

    def update(self):
        super().update()
        getsCustomer = False
        time1 = pygame.time.get_ticks()
        if time1 - self.currentTime >= self.interval:
            self.currentTime = pygame.time.get_ticks()
            getsCustomer = (random.randint(0,GameData.newCustomerChance) == 1)
        
        if getsCustomer:
            getsCustomer = False
            newPatient = {
                "id" : len(GameData.activePatients),
                "species" : "cat",
                "walkingAnimation" : patientInfo["cat"]["walkingAnimation"],
                "idleAnimation" : patientInfo["cat"]["idleAnimation"],
                "talkingAnimation" : patientInfo["cat"]["talkingAnimation"],
                "state" : "walking",
                "pos" : [1500,350],
                "targetPos" : random.randint(100,1200),
                "speed" : random.randint(2,5),
                "illness" : random.choice(patientInfo["cat"]["potentialIllnesses"])
            }
            GameData.activePatients.append(newPatient)
            for state in stateManager.queue:
                if type(state) == PatientRoomState:
                    state.updatePatients()



class PatientRoomState(State):
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/backgroundmain.png"), (orig_size[0], orig_size[1]))
        self.desk = pygame.transform.smoothscale_by(pygame.image.load("images/mainroom/desk.png").convert_alpha(), .4)
        self.patients = []
        for patient in GameData.activePatients:
            self.patients.append(Patient(patient["walkingAnimation"], patient["idleAnimation"], patient["talkingAnimation"], patient["state"], patient["pos"], patient["targetPos"], patient["speed"], patient["id"]))
        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIconClosed = MapButton(True)
        self.coins = Coins()
        self.book = Book()
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed, self.coins]

    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        for patient in self.patients:
            patient.render(self.surface)
        self.surface.blit(self.desk, (30, 40))
        self.surface.blit(self.desk, (30, 40))
        self.book.render(self.surface)
        screen.blit(self.surface, offset)
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
                    stateManager.transition(True)
                    stateManager.push(PotionRoomState())
                if self.rightArrow.checkClick():
                    stateManager.transition(False)
                    stateManager.push(GardenState())
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())
    
    def updatePatients(self):
        if len(GameData.activePatients) > len(self.patients):
            for i in range(len(self.patients), len(GameData.activePatients)):
                patient = GameData.activePatients[i]
                self.patients.append(Patient(patient["walkingAnimation"], patient["idleAnimation"], patient["talkingAnimation"], patient["state"], patient["pos"], patient["targetPos"], patient["speed"], patient["id"]))



class PotionRoomState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/potionroom.png"), (orig_size[0], orig_size[1]))
        self.cauldron = Cauldron([530, 250])
        self.table = pygame.Surface((400,200))
        self.table.fill((64, 61, 57))
        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIconClosed = MapButton(True)
        self.coins = Coins()
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed, self.coins]
    
    def update(self):
        super().update()
        self.cauldron.update()

    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        self.cauldron.render(self.surface)

        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rightArrow.checkClick():
                    stateManager.transition(False)
                    stateManager.push(PatientRoomState())
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())
                if self.cauldron.checkClick():
                    stateManager.push(PotionMakingState())


class PotionMakingState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.smoothscale_by(pygame.image.load("images/backgrounds/brew_background.png"), .42)
        self.cauldron = Cauldron((-120,-100), 1.75)
        self.ingredientMenu = PotionIngredientMenu()

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.background, (0,0))
        screen.blit(self.background, (0,0))
        self.cauldron.render(screen)
        self.ingredientMenu.render(screen)
    
    def update(self):
        super().update()
        self.cauldron.update()
    
    def handleInput(self, events):
        super().handleInput(events)



class GardenState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.Surface([orig_size[0], orig_size[1]])
        self.background.fill((182, 204, 254))
        pygame.draw.rect(self.background, (132, 169, 140), (0, 600, 1600, 500))
        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIconClosed = MapButton(True)
        self.coins = Coins()
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed, self.coins]

    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)


    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.transition(True)
                    stateManager.push(PatientRoomState())
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())



class MapState(State):
    def __init__(self):
        super().__init__()
        self.map = pygame.transform.smoothscale_by(pygame.image.load("images/ui/mapui.png"), .6)
        self.rect = pygame.Rect(380,180,830,520)
        self.darkbg = pygame.Surface(orig_size)
        self.darkbg.fill((0,0,0))
        self.darkbg.set_alpha(90)
        self.mapIcon = MapButton(False)
        self.roomMap = pygame.transform.smoothscale_by(pygame.image.load("images/ui/room_map.png"), .25)

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.darkbg, (0,0))
        screen.blit(self.map, (310,130))
        screen.blit(self.roomMap, (330,200))
        self.mapIcon.render(screen)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
    

