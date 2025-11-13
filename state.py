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

            if len(GameData.activePatients) < 7:
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
        self.brewButton = BrewButton()

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.background, (0,0))
        screen.blit(self.background, (0,0))
        self.cauldron.render(screen)
        self.ingredientMenu.render(screen)
        self.xButton.render(screen)
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

    def handleInput(self, events):
        super().handleInput(events)
        self.ingredientMenu.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
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

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.darkbg, (0,0))
        screen.blit(self.map, (310,130))
        screen.blit(self.roomMap, (330,200))
        self.mapIcon.render(screen)

        pygame.draw.rect(screen, (255,0,0), self.patientRoomRect1, 2)
    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
                
                if self.patientRoomRect1.collidepoint(pos):
                    stateManager.push(PatientRoomState())
    


class PatientRoomState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/backgroundmain.png"), (orig_size[0], orig_size[1]))
        self.patient = None
        self.inventoryButton = InventoryButton()

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.background, (0,0))
        self.inventoryButton.render(screen)

    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventoryButton.checkClick():
                    stateManager.push(InventoryOpenState())



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

        self.potions = []
        for i, potion in enumerate(GameData.potionsInInventory):
            self.potions.append(PotionItemInInventory(potion, (100+i*100, self.pos[1] + 60)))


    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.image, self.pos)
        self.xButton.render(screen)

        for potion in self.potions:
            potion.render(screen)

    def update(self):
        super().update()
        if self.transitioningIn:
            self.t += 1
            self.pos[1] = 2 * (self.t ** 2) + 550
            self.xButton.pos[1] = self.pos[1] - 20
            for potion in self.potions:
                potion.pos[1] = self.pos[1] + 80
                potion.rect.y = potion.pos[1]
            if self.t >= 5:
                self.transitioningIn = False
        
        if self.transitioningOut:
            self.t -= 1
            self.pos[1] = 2 * (self.t ** 2) + 550
            self.xButton.pos[1] = self.pos[1] - 20
            for potion in self.potions:
                potion.pos[1] = self.pos[1] + 80
                potion.rect.y = potion.pos[1]
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


