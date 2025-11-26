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
        self.everythingState.update()
        self.everythingState.render(surface, [0,0])
        self.everythingState.handleInput(events)
        if not self.transitioning:
            self.queue[len(self.queue)-1].update()
            if len(self.queue) > 1:
                self.queue[len(self.queue)-2].render(surface, [0,0])
            self.queue[len(self.queue)-1].render(surface, [0,0])
            self.queue[len(self.queue)-1].handleInput(events)
        else:
            self.queue[len(self.queue)-1].update()
            self.queue[len(self.queue)-2].update()
            self.queue[len(self.queue)-1].render(surface, self.bgNewOffset)
            self.queue[len(self.queue)-2].render(surface, self.bgOldOffset)
            movement = (self.bgNewOffset[0])/6
            if abs(movement) < 5:
                movement = 5 * (movement/abs(movement))
            self.bgNewOffset[0] -= movement
            self.bgOldOffset[0] -= movement
            if self.bgNewOffset[0] > -6 and self.bgNewOffset[0] < 6:
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

            if len(GameData.activePatients) < GameData.customerLimit:
                newPatient = Patient(
                    patientInfo["cat"]["walkingAnimation"],
                    patientInfo["cat"]["idleAnimation"],
                    patientInfo["cat"]["talkingAnimation"],
                    "walking",
                    [1500,350],
                    random.randint(100,1200),
                    random.randint(2,5),
                    len(GameData.activePatients),
                    random.choice(patientInfo["cat"]["potentialIllnesses"])
                )
                GameData.activePatients.append(newPatient)
                for state in stateManager.queue:
                    if type(state) == WaitingRoomState:
                        state.updatePatients()


class WaitingRoomState(State):
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/backgroundmain.png"), (orig_size[0], orig_size[1]))
        self.desk = pygame.transform.smoothscale_by(pygame.image.load("images/mainroom/desk.png").convert_alpha(), .4)
        self.patients = []
        for patient in GameData.activePatients:
            self.patients.append(patient)
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

        for patient in self.patients:
            if patient not in GameData.activePatients:
                self.patients.remove(patient)
                break
    


    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.transition(True)
                    stateManager.push(PotionRoomState())
                if self.rightArrow.checkClick():
                    stateManager.transition(False)
                    stateManager.push(GardenState("garden 1"))
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())
                
                for patient in GameData.activePatients:
                    if patient.currentState != "walking":
                        if patient.checkClick():
                            stateManager.push(PatientPopupState(patient))

    def updatePatients(self):
        if len(GameData.activePatients) > len(self.patients):
            for i in range(len(self.patients), len(GameData.activePatients)):
                patient = GameData.activePatients[i]
                self.patients.append(patient)

class PatientPopupState(State):
    def __init__(self, patient):
        super().__init__()
        self.background = pygame.Surface((500, 700))
        self.background.fill((220,200,180))
        self.rect = pygame.Rect(40,40, 500,700)
        self.patient = patient

        self.rects = []
        for i in range(8):
            self.rects.append(pygame.Rect(60+(i%4)*60, 450+(i//4)*60, 55,55))

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.background, self.rect.topleft)
        textRenderer.render(screen, self.patient.illness, (60, 150), 40, (255,255,255))
        for rect in self.rects:
            pygame.draw.rect(screen, (0,255,0), rect)
    

    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
                
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        GameData.patientsInRooms[i] = self.patient
                        GameData.activePatients.remove(self.patient)
                        stateManager.pop()

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
                    stateManager.push(WaitingRoomState())
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())
                if self.cauldron.checkClick():
                    stateManager.push(PotionMakingState())


class PotionMakingState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.smoothscale_by(pygame.image.load("images/backgrounds/brew_background.png"), .42)
        self.cauldron = Cauldron((-120,-100), 1.75)
        self.window = pygame.Surface((600,150))
        self.window.fill((200,200,200))
        self.ingredientMenu = PotionIngredientMenu()
        self.xButton = XButton((5,5))
        self.draggingItem = None
        self.ingredients = []
        self.ingredientsText = []
        self.brewButton = BrewButton()
        self.canBrew = False
        self.currentPotion = None

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.background, (0,0))
        screen.blit(self.background, (0,0))
        self.cauldron.render(screen)
        self.ingredientMenu.render(screen)
        self.xButton.render(screen)

        if self.canBrew:
            self.brewButton.render(screen)

        screen.blit(self.window, (500,740))
        for ingredient in self.ingredients:
            ingredient.render(screen)

        if self.draggingItem != None:
            self.draggingItem.render(screen)
        


    def update(self):
        super().update()
        self.cauldron.update()
        self.ingredientMenu.update()

        for potion in potionInfo["potions"].keys():
            if potionInfo["potions"][potion]["recipe"] == self.ingredientsText:
                self.currentPotion = potion
                self.canBrew = True

    def handleInput(self, events):
        super().handleInput(events)
        self.ingredientMenu.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.canBrew:
                    if self.brewButton.checkClick():
                        potionInInventory = False
                        for i, potion in enumerate(GameData.potionsInInventory):
                            if potion["name"] == self.currentPotion:
                                GameData.potionsInInventory[i]["quantity"] += 1
                                potionInInventory = True
                                break
                        if not potionInInventory:
                            GameData.potionsInInventory.append(
                                {
                                    "name" : self.currentPotion,
                                    "quantity" : 1
                                }
                            )
                        self.currentPotion = None
                        self.ingredients = []
                        self.ingredientsText = []
                        self.canBrew = False

                if self.xButton.checkClick():
                    stateManager.pop()

                left_page_index = self.ingredientMenu.currentPageSet * 2
                right_page_index = left_page_index + 1
                
                # left page
                leftPage = self.ingredientMenu.pages[left_page_index]

                # right page
                rightPage = self.ingredientMenu.pages[right_page_index]


                for ingredient in leftPage.ingredients:
                    if ingredient.checkClick():
                        if ingredient.quantity > 0:
                            self.draggingItem = PotionIngredientDragging(ingredient.image, ingredient.category, ingredient.name, (pygame.mouse.get_pos()[0]-ingredient.rect.x, pygame.mouse.get_pos()[1]-ingredient.rect.y))
                            ingredient.quantity -= 1

                for ingredient in rightPage.ingredients:
                    if ingredient.checkClick():
                        if ingredient.quantity > 0:
                            self.draggingItem = PotionIngredientDragging(ingredient.image, ingredient.category, ingredient.name, (pygame.mouse.get_pos()[0]-ingredient.rect.x, pygame.mouse.get_pos()[1]-ingredient.rect.y))
                            ingredient.quantity -= 1




            if event.type == pygame.MOUSEBUTTONUP:
                if self.draggingItem != None:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(450,1150) and pos[1] < 600:
                        self.ingredients.append(PotionIngredientInCauldron(
                            self.draggingItem.image, 
                            self.draggingItem.category, 
                            self.draggingItem.name, 
                            (pos[0]-self.draggingItem.offset[0], pos[1]-self.draggingItem.offset[1]),
                            (570+(len(self.ingredients))*90, 760)
                        ))
                        self.ingredientsText.append(self.draggingItem.name)
                    else:
                        left_page_index = self.ingredientMenu.currentPageSet * 2
                        right_page_index = left_page_index + 1
                        
                        # left page
                        leftPage = self.ingredientMenu.pages[left_page_index]

                        # right page
                        rightPage = self.ingredientMenu.pages[right_page_index]


                        for ingredient in leftPage.ingredients:
                            if ingredient.name == self.draggingItem.name:
                                ingredient.quantity += 1

                        for ingredient in rightPage.ingredients:
                            if ingredient.name == self.draggingItem.name:
                                ingredient.quantity += 1
                    self.draggingItem = None


class GardenState(State):
    def __init__(self, garden):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.Surface([orig_size[0], orig_size[1]])
        self.background.fill((182, 204, 254))
        pygame.draw.rect(self.background, (132, 169, 140), (0, 600, 1600, 500))
        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIconClosed = MapButton(True)
        self.inventoryButton = InventoryButton()
        self.coins = Coins()
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed, self.coins]
        self.garden = garden
        self.plants = GameData.gardenData[self.garden]["plots"]


    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        for plant in self.plants:
            if plant != None:
                plant.render(self.surface)
        self.inventoryButton.render(self.surface)
        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)


    def update(self):
        super().update()
        for plant in self.plants:
            if plant != None:
                plant.update()


    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventoryButton.checkClick():
                    stateManager.push(SeedInventoryOpenState())
                if self.leftArrow.checkClick():
                    stateManager.transition(True)
                    stateManager.push(WaitingRoomState())
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

        self.patientRoomRect1 = pygame.Rect(645,365,80,80)
        self.patientRoomRect2 = pygame.Rect(730, 365, 80,80)
        self.patientRoomRect3 = pygame.Rect(810, 365, 80, 80)
        self.patientRoomRect4 = pygame.Rect(890, 365, 80,80)
        self.patientRoomRect5 = pygame.Rect(645, 445, 80,80)
        self.patientRoomRect6 = pygame.Rect(730, 445, 80,80)
        self.patientRoomRect7 = pygame.Rect(810, 445, 80,80)
        self.patientRoomRect8 = pygame.Rect(890, 445, 80,80)

        self.roomRects = [
            self.patientRoomRect1,
            self.patientRoomRect2,
            self.patientRoomRect3,
            self.patientRoomRect4,
            self.patientRoomRect5,
            self.patientRoomRect6,
            self.patientRoomRect7,
            self.patientRoomRect8
        ]

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.darkbg, (0,0))
        screen.blit(self.map, (310,130))
        screen.blit(self.roomMap, (330,200))
        self.mapIcon.render(screen)

        # for rect in self.roomRects:
        #     pygame.draw.rect(screen, (255,0,0), rect, 2)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
                
                for i in range(len(self.roomRects)):
                    if self.roomRects[i].collidepoint(pos):
                        stateManager.push(PatientRoomState(i))


class PatientRoomState(State):
    def __init__(self, index):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.index = index
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/backgroundmain.png"), (orig_size[0], orig_size[1]))
        self.patient = GameData.patientsInRooms[self.index]
        self.inventoryButton = InventoryButton()
        self.patient = GameData.patientsInRooms[self.index]

        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIconClosed = MapButton(True)
        self.coins = Coins()
        self.uiElements = [self.leftArrow, self.rightArrow, self.mapIconClosed, self.coins]


    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        if self.patient != None:
            self.patient.render(self.surface)
        self.inventoryButton.render(self.surface)
        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)

    def update(self):
        super().update()
        if self.patient != None:
            self.patient.update()

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventoryButton.checkClick():
                    stateManager.push(PotionInventoryOpenState())
                if self.leftArrow.checkClick():
                    stateManager.transition(True)
                    stateManager.push(PatientRoomState(self.index-1))
                if self.rightArrow.checkClick():
                    stateManager.transition(False)
                    stateManager.push(PatientRoomState(self.index+1))
                if self.mapIconClosed.checkClick():
                    stateManager.push(MapState())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE or pygame.K_BACKSPACE:
                    stateManager.pop()


class InventoryOpenState(State):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1500,300))
        self.image.fill((175,175,175))
        self.xButton = XButton((20,600))
        self.pos = [40,600]
        self.transitioningIn = True
        self.transitioningOut = False
        self.t = -20


    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.image, self.pos)
        self.xButton.render(screen)

    def update(self):
        super().update()
        if self.transitioningIn:
            self.t += 1
            self.pos[1] = 2 * (self.t ** 2) + 550
            self.xButton.pos[1] = self.pos[1] - 20
            if self.t >= 5:
                self.transitioningIn = False
        
        if self.transitioningOut:
            self.t -= 1
            self.pos[1] = 2 * (self.t ** 2) + 550
            self.xButton.pos[1] = self.pos[1] - 20
            if self.t <= -20:
                self.transitioningOut = False
                stateManager.pop()

    def handleInput(self, events):
        super().handleInput(events)
        if not self.transitioningIn and not self.transitioningOut:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.xButton.checkClick():
                        self.transitioningOut = True


class PotionInventoryOpenState(InventoryOpenState):
    def __init__(self):
        super().__init__()
        self.potions = []
        for i, potion in enumerate(GameData.potionsInInventory):
            self.potions.append(PotionItemInInventory(potion, (100+i*100, self.pos[1] + 60)))

    def render(self, screen, offset):
        super().render(screen, offset)
        for potion in self.potions:
            potion.render(screen)
    
    def update(self):
        super().update()
        if self.transitioningIn:
            for potion in self.potions:
                potion.pos[1] = self.pos[1] + 80
                potion.rect.y = potion.pos[1]
        if self.transitioningOut:
            for potion in self.potions:
                potion.pos[1] = self.pos[1] + 80
                potion.rect.y = potion.pos[1]

    def handleInput(self, events):
        super().handleInput(events)


class SeedInventoryOpenState(InventoryOpenState):
    def __init__(self):
        super().__init__()
        self.seeds = []
        for i, seed in enumerate(GameData.seedInventory):
            self.seeds.append(SeedItemInInventory(seed, (100+i*100, self.pos[1] + 60)))

    def render(self, screen, offset):
        super().render(screen, offset)
        for seed in self.seeds:
            seed.render(screen)
    
    def update(self):
        super().update()
        if self.transitioningIn:
            for seed in self.seeds:
                seed.pos[1] = self.pos[1] + 80
                seed.rect.y = seed.pos[1]
        if self.transitioningOut:
            for seed in self.seeds:
                seed.pos[1] = self.pos[1] + 80
                seed.rect.y = seed.pos[1]

    def handleInput(self, events):
        super().handleInput(events)