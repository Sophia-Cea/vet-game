from otherClasses import *

class StateManager:
    def __init__(self) -> None:
        self.queue = []
        self.transitioning = False
        self.transitioningLeft = None
        self.transitioningDown = None
        self.bgOldOffset = [0,0]
        self.bgNewOffset = [0,0]
        self.everythingState = None

    def push(self, page):
        self.queue.append(page)
        page.onEnter()

    def transition(self, transitioningLeft, transitioningDown=None):
        self.transitioning = True
        self.transitioningLeft = transitioningLeft
        self.transitioningDown = transitioningDown
        if self.transitioningLeft == True:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [-WIDTH,0]
        elif self.transitioningLeft == False:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [WIDTH,0]
        
        if self.transitioningDown == True:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [0,HEIGHT]
        elif self.transitioningDown == False:
            self.bgOldOffset = [0,0]
            self.bgNewOffset = [0,-HEIGHT]


    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)
        

    def run(self, surface, events):
        self.everythingState.update()
        self.everythingState.render(surface, [0,0])
        self.everythingState.handleInput(events)
        if not self.transitioning:
            self.queue[len(self.queue)-1].update()
            for state in self.queue:
                state.render(surface, [0,0])
            self.queue[len(self.queue)-1].handleInput(events)
        else:
            self.queue[len(self.queue)-1].update()
            self.queue[len(self.queue)-2].update()
            self.queue[len(self.queue)-1].render(surface, self.bgNewOffset)
            self.queue[len(self.queue)-2].render(surface, self.bgOldOffset)
            if self.transitioningLeft != None:
                movement = (self.bgNewOffset[0])/6
                if abs(movement) < 5:
                    movement = 5 * (movement/abs(movement))
                self.bgNewOffset[0] -= movement
                self.bgOldOffset[0] -= movement
                if self.bgNewOffset[0] > -6 and self.bgNewOffset[0] < 6:
                    self.transitioning = False
                    self.transitioningLeft = None
                    self.queue.remove(self.queue[-2])
            
            if self.transitioningDown != None:
                movement = (self.bgNewOffset[1])/6
                if abs(movement) < 5:
                    movement = 5 * (movement/abs(movement))
                self.bgNewOffset[1] -= movement
                self.bgOldOffset[1] -= movement
                if self.bgNewOffset[1] > -6 and self.bgNewOffset[1] < 6:
                    self.transitioning = False
                    self.transitioningDown = None
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
            for state in stateManager.queue:
                if type(state) == WaitingRoomState:
                    state.arrivePatient()
            getsCustomer = False

            if len(GameData.activePatients) < GameData.customerLimit:
                
                # --- START NEW WEIGHTED LOGIC ---
                all_animals = []
                all_weights = []
                
                # Iterate through the nested dictionary to build our lists
                for category in GameData.animalData.values():
                    for animal, weight in category.items():
                        all_animals.append(animal)
                        all_weights.append(weight)

                # Pick the animal
                chosen_animal = random.choices(all_animals, weights=all_weights, k=1)[0]
                # --- END NEW WEIGHTED LOGIC ---

                newPatient = Patient(
                    # Use chosen_animal instead of "cat"
                    patientInfo[chosen_animal]["walkingAnimation"],
                    patientInfo[chosen_animal]["idleAnimation"],
                    patientInfo[chosen_animal]["talkingAnimation"],
                    "walking",
                    [1500, 220],
                    random.randint(100, 1200),
                    random.randint(4, 7),
                    len(GameData.activePatients),
                    # Also use chosen_animal for the illness lookup
                    random.choice(patientInfo[chosen_animal]["potentialIllnesses"])
                )
                GameData.activePatients.append(newPatient)
                for state in stateManager.queue:
                    if type(state) == WaitingRoomState:
                        state.updatePatients()


class SettingsOpenState(State):
    def __init__(self):
        super().__init__()
        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(150)
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/Settings_UI.png"), .4)
        self.rect = pygame.Rect(470,125,670,590)
        self.pos = [440,90]

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.backgroundDark, (0,0))
        screen.blit(self.image, self.pos)
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        textRenderer.render(screen, "Settings", (800, 200), 45, (40,20,10), align="center")

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(pos):
                    stateManager.pop()

class WaitingRoomState(State):
    def __init__(self) -> None:
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        
        self.background = pygame.transform.smoothscale(pygame.image.load("images/mainroom/background_main.png"), (orig_size[0], orig_size[1])).convert() # Use .convert()!
        self.floor = pygame.transform.smoothscale(pygame.image.load("images/mainroom/floor.png"), (orig_size[0], orig_size[1])).convert_alpha()
        self.woodFrame = pygame.transform.smoothscale(pygame.image.load("images/mainroom/woodframe.png"), (orig_size[0], orig_size[1])).convert_alpha()
        self.fireplacebricks = pygame.transform.smoothscale(pygame.image.load("images/mainroom/fireplace_outside.png"), (orig_size[0], orig_size[1])).convert_alpha()
        self.fireplaceinside = pygame.transform.smoothscale(pygame.image.load("images/mainroom/fireplace_inside.png"), (orig_size[0], orig_size[1])).convert_alpha()
        self.desk = pygame.transform.smoothscale_by(pygame.image.load("images/mainroom/deskNew.png"), .4).convert_alpha()
        
        self.doorClosed = pygame.transform.smoothscale(pygame.image.load("images/mainroom/door_closed.png"), (orig_size[0], orig_size[1]))
        self.doorOpen = pygame.transform.smoothscale(pygame.image.load("images/mainroom/door_open.png"), (orig_size[0], orig_size[1]))
        self.doorwayRight = pygame.transform.smoothscale(pygame.image.load("images/mainroom/doorway_right.png"), (orig_size[0], orig_size[1]))
        self.fire = Animation("images/mainroom/fire/", [
            "fire1.png",
            "fire2.png",
            "fire3.png",
            "fire4.png",
            "fire5.png",
            "fire6.png",
            "fire7.png",
            "fire8.png"
        ], 1, .15)

        self.background.blit(self.floor, (0,0))
        self.background.blit(self.woodFrame, (0,0))
        self.background.blit(self.fireplaceinside, (0,0))


        self.patients = []
        for patient in GameData.activePatients:
            self.patients.append(patient)
        self.inventoryButton = InventoryButton()
        self.leftArrow = Arrow(True)
        self.mapIcon = MapButton()
        self.downArrow = VerticalArrow(True)
        self.coins = Coins()
        self.book = Book()
        self.settings = SettingsButton()
        self.uiElements = [self.leftArrow, self.downArrow, self.mapIcon, self.coins, self.inventoryButton, self.settings]
        self.backgroundColor = (222, 201, 168)
        self.doorRect = pygame.Rect(1400,150,150,550)
        self.patientArriving = False
        self.patientArrivingTime = None

    def arrivePatient(self):
        self.patientArriving = True
        self.patientArrivingTime = datetime.now()


    def render(self, screen, offset):
        super().render(screen, offset)
        pos = pygame.mouse.get_pos()
        self.surface.blit(self.background, (0,0))

        self.fire.render(self.surface, (680,330))
        self.surface.blit(self.fireplacebricks, (0,0))

        if self.doorRect.collidepoint(pos) or self.patientArriving:
            self.surface.blit(self.doorOpen, (0,0))

        else:
            self.surface.blit(self.doorClosed, (0,0))
        
        for patient in self.patients:
            patient.render(self.surface)
        
        pygame.draw.rect(self.surface, self.backgroundColor, (1550,100,200,630))
        self.surface.blit(self.doorwayRight, (0,0))


        self.surface.blit(self.desk, (30, 40))
        self.surface.blit(self.desk, (30, 40))
        self.book.render(self.surface)
        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)

        # pygame.draw.rect(screen, (255,0,0), self.doorRect, 2)


    def update(self):
        super().update()
        self.fire.update()
        for patient in self.patients:
            patient.update()

        for patient in self.patients:
            if patient not in GameData.activePatients:
                self.patients.remove(patient)
                break
        
        if self.patientArriving:
            current_real_time = datetime.now()
            time_elapsed = current_real_time - self.patientArrivingTime
            required_duration = timedelta(seconds=5)
            if time_elapsed >= required_duration:
                self.patientArriving = False
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.transition(True)
                    stateManager.push(PotionRoomState())
                if self.downArrow.checkClick():
                    stateManager.transition(None, True)
                    stateManager.push(PatientRoomState(0))
                if self.mapIcon.checkClick():
                    self.mapIcon.isClosed = False
                    stateManager.push(MapState())
                if self.settings.checkClick():
                    stateManager.push(SettingsOpenState())
                
                for patient in GameData.activePatients:
                    if patient.currentState != "walking":
                        if patient.checkClick():
                            # stateManager.push(PatientPopupState(patient))
                            stateManager.push(DialogueState(patient))
                            break
                            # stateManager.push(RelocatePopupState(patient))
                
                if self.inventoryButton.checkClick():
                    self.inventoryButton.closed = False
                    stateManager.push(InventoryOpenState())

    def updatePatients(self):
        if len(GameData.activePatients) > len(self.patients):
            for i in range(len(self.patients), len(GameData.activePatients)):
                patient = GameData.activePatients[i]
                self.patients.append(patient)

class PotionRoomState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/potionroom.png"), (orig_size[0], orig_size[1]))
        self.cauldron = Cauldron([535, 322])
        self.table = pygame.Surface((400,200))
        self.table.fill((64, 61, 57))
        self.inventoryButton = InventoryButton()
        self.rightArrow = Arrow(False)
        self.mapIcon = MapButton()
        self.coins = Coins()
        self.settings = SettingsButton()
        self.uiElements = [self.rightArrow, self.mapIcon, self.coins, self.inventoryButton, self.settings]

    def update(self):
        super().update()
        self.cauldron.update()

    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.fill((0,0,80))
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
                if self.mapIcon.checkClick():
                    self.mapIcon.isClosed = False
                    stateManager.push(MapState())
                if self.cauldron.checkClick():
                    stateManager.push(PotionMakingState())
                if self.settings.checkClick():
                    stateManager.push(SettingsOpenState())
                
                if self.inventoryButton.checkClick():
                    self.inventoryButton.closed = False
                    stateManager.push(InventoryOpenState())


class PotionMakingState(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.transform.smoothscale_by(pygame.image.load("images/backgrounds/brew_background.png"), .42)
        self.cauldron = Cauldron((-120,-100), 1.75)
        self.ingredientLimit = 5
        self.window = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/ui/ingredientHolder.png"), .2)
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

        screen.blit(self.window, (480,680))
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
                if self.ingredientMenu.draggingItem != None:
                    self.draggingItem = self.ingredientMenu.draggingItem
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


            if event.type == pygame.MOUSEBUTTONUP:
                if self.draggingItem != None:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(450,1150) and pos[1] < 600:
                        if len(self.ingredients) < self.ingredientLimit: 
                            self.ingredients.append(PotionIngredientInCauldron(
                                self.draggingItem.image, 
                                self.draggingItem.name, 
                                (pos[0]-self.draggingItem.offset[0], pos[1]-self.draggingItem.offset[1]),
                                (570+(len(self.ingredients))*90, 760)
                            ))
                            self.ingredientsText.append(self.draggingItem.name)
                    
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
        self.mapIcon = MapButton()
        self.inventoryButton = InventoryButton()
        self.coins = Coins()
        self.upArrow = VerticalArrow(False)
        self.settings = SettingsButton()
        self.uiElements = [self.leftArrow, self.rightArrow, self.upArrow, self.mapIcon, self.coins, self.inventoryButton, self.settings]
        self.garden = garden
        self.plots = [
            GardenPlot((300, 550), self.garden, 0), GardenPlot((600,550), self.garden, 1), GardenPlot((900,550), self.garden, 2)
        ]


    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        for plot in self.plots:
            plot.render(self.surface, (0,0))
        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)

    def update(self):
        super().update()
        for i, plot in enumerate(self.plots):
            plot.update()
            if plot.diggingUp == True:
                stateManager.push(AreYouSureDigUpState(self.garden, i))
            if plot.planting == True:
                stateManager.push(GardenPlotPopupState(self.garden, i))

        
        for i, plot in enumerate(self.plots):
            gamedataPlant = GameData.gardenData[self.garden]["plots"][i]["plant"]
            if plot.plant == None and gamedataPlant != None:
                plot.plant = gamedataPlant
            if plot.plant != None and gamedataPlant == None:
                plot.plant = gamedataPlant
    
        

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()

        for plot in self.plots:
            plot.handleInput(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inventoryButton.checkClick():
                    self.inventoryButton.closed = False
                    stateManager.push(InventoryOpenState())
                if self.settings.checkClick():
                    stateManager.push(SettingsOpenState())


                if self.mapIcon.checkClick():
                    self.mapIcon.isClosed = False
                    stateManager.push(MapState())
                if self.upArrow.checkClick():
                    stateManager.transition(None, False)
                    stateManager.push(PatientRoomState(0))

    

class Garden1(GardenState):
    def __init__(self):
        super().__init__("garden 1")
        self.uiElements.remove(self.leftArrow)
        self.beehive = Beehive()
        img = pygame.image.load("images/backgrounds/Garden1.png").convert_alpha()
        self.background = pygame.transform.smoothscale_by(img, 0.45)
        

    def render(self, screen, offset):
        super().render(screen, offset)
        self.beehive.render(self.surface)

        screen.blit(self.surface, offset)
        for element in self.uiElements:
            element.render(screen)


    def update(self):
        super().update()
        self.beehive.update()

        

    def handleInput(self, events):
        super().handleInput(events)
        self.beehive.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rightArrow.checkClick():
                    stateManager.transition(False, None)
                    stateManager.push(Garden2())


class Garden2(GardenState):
    def __init__(self):
        super().__init__("garden 2")
        self.uiElements.remove(self.rightArrow)

        img = pygame.image.load("images/backgrounds/Garden2.png").convert_alpha()
        self.background = pygame.transform.smoothscale_by(img, 0.45)

        self.gateRect = pygame.Rect(1260, 350, 270, 380)
        self.interactive_rects = [self.gateRect]

        self.transitioningOut = False
        self.transitioningIn = False
        self.transitionScreen = pygame.Surface((WIDTH, HEIGHT))
        self.opacity = 0
        self.transitionSpeed = 10


    def get_hover_rects(self):
        return self.interactive_rects

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.transitionScreen, (0,0))
        self.transitionScreen.set_alpha(self.opacity)

    def update(self):
        super().update()
        if self.transitioningIn:
            self.opacity -= self.transitionSpeed
            if self.opacity <= 0:
                self.transitioningIn = False
                self.opacity = 0
        if self.transitioningOut:
            self.opacity += self.transitionSpeed
            if self.opacity >= 255:
                self.opacity = 255
                self.transitioningOut = False
                stateManager.push(ForestState())

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    stateManager.transition(True, None)
                    stateManager.push(Garden1())
                if self.gateRect.collidepoint(pos):
                    self.transitioningOut = True


class GardenPlotPopupState(State):
    def __init__(self, garden, index):
        self.garden = garden
        self.index = index
        self.backgroundImg = pygame.transform.smoothscale_by(pygame.image.load("images/ui/Settings_UI.png"), .4)
        self.borderImg = None
        self.scrollBar = ScrollBar(
            pygame.Rect(1070,280, 25, 360), 
            pygame.Rect(1075, 283, 15, 100), 
            (120,110,100), (160,140,130)
        )
        self.seeds = []
        self.pos = (440,100)
        for i, seed in enumerate(GameData.seedInventory):
            self.seeds.append(SeedItemInInventory(seed, (self.pos[0] + 55 + 110*(i%6), self.pos[1] + 180 + (i//6) * 110)))

        self.choice = None

        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(150)
        self.rect = pygame.Rect(475,140,665,585)
        self.surface = pygame.Surface((670,590), pygame.SRCALPHA)


    def render(self, screen, offset):
        screen.blit(self.backgroundDark, (0,0))
        self.surface.blit(self.backgroundImg,(-30,-40))
        for seed in self.seeds:
            seed.render(self.surface, self.scrollBar.offset)
        screen.blit(self.surface, (475, 140))
        
        
        self.scrollBar.render(screen)

        textRenderer.render(screen, "Choose a Seed to Plant", (600,200), 35, (40,20,10))
        
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)

    def update(self):
        self.scrollBar.update()

        if self.choice != None:
            for i, seed in enumerate(GameData.seedInventory):
                if seed["name"] == self.choice.name:
                    GameData.seedInventory[i]["quantity"] -= 1
                    if GameData.seedInventory[i]["quantity"] <= 0:
                        GameData.seedInventory.remove(seed)
                    break
                    
            GameData.gardenData[self.garden]["plots"][self.index]["plant"] = GardenPlant(self.choice.name, (300+self.index*300))
            stateManager.pop()
            stateManager.queue[-1].plots[self.index].planting = False

    def handleInput(self, events):
        self.scrollBar.handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for seed in self.seeds:
                    if seed.rect.collidepoint(pos):
                        self.choice = seed

                if not self.rect.collidepoint(pos):
                    stateManager.pop()
                    stateManager.queue[-1].plots[self.index].planting = False



class AreYouSurePopupState(State):
    def __init__(self, question):
        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(150)

        self.popup = pygame.Surface((400,300))
        self.popup.fill((200,180,150))
        self.rect = pygame.Rect(600,250,400,300)
        self.answer = None
        self.question = question

        self.button = pygame.Surface((100,50))
        self.button.fill((200,180,150))
        pygame.draw.rect(self.button, (40,20,10), (0,0,100,50), 4)

        self.yesRect = pygame.Rect(650,470, 100,50)
        self.noRect = pygame.Rect(910, 470, 100, 60)

    def render(self, screen, offset):
        screen.blit(self.backgroundDark, (0,0))


        textRenderer.render(self.popup, "Are you sure you want to", (200,30), 25, (40,20,10), align="center")
        textRenderer.render(self.popup, self.question + "?", (200,60), 25, (40,20,10), align="center")

        self.popup.blit(self.button, (50, 220))
        self.popup.blit(self.button, (310, 220))

        textRenderer.render(self.popup, "Yes", (60, 235), 15, (40,20,10), align="center")
        textRenderer.render(self.popup, "No", (340, 235), 15, (40,20,10), align="center")

        screen.blit(self.popup, (self.rect.x,self.rect.y))

        # pygame.draw.rect(screen, (255,0,0), self.yesRect, 2)
        # pygame.draw.rect(screen, (255,0,0), self.noRect, 2)

        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)


    def update(self):
        pass

    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(pos):
                    pass
                if self.yesRect.collidepoint(pos):
                    self.answer = True
                if self.noRect.collidepoint(pos):
                    self.answer = False
                

class AreYouSureDigUpState(AreYouSurePopupState):
    def __init__(self, garden, index):
        super().__init__("dig up plant")
        self.garden = garden
        self.index = index

    def update(self):
        super().update()
        if self.answer!= None:
            if self.answer == True:
                # print("said yes")
                GameData.gardenData[self.garden]["plots"][self.index]["plant"] = None
            elif self.answer == False:
                # print("said no")
                pass

            stateManager.pop()
            stateManager.queue[-1].plots[self.index].diggingUp = False
    
    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
                    stateManager.queue[-1].plots[self.index].diggingUp = False

        













class MapState(State):
    def __init__(self):
        super().__init__()
        self.map = pygame.transform.smoothscale_by(pygame.image.load("images/ui/mapui.png"), .6)
        self.rect = pygame.Rect(380,180,830,520)
        self.darkbg = pygame.Surface(orig_size)
        self.darkbg.fill((0,0,0))
        self.darkbg.set_alpha(90)
        # self.mapIcon = MapButton(False)
        self.roomMap = pygame.transform.smoothscale_by(pygame.image.load("images/ui/room_map.png"), .25)
        self.lockImageShort = pygame.transform.smoothscale_by(pygame.image.load("images/ui/lock_short.png"), .25)
        self.lockImageLong = pygame.transform.smoothscale_by(pygame.image.load("images/ui/lock_long.png"), .25)


        self.patientRoomRect1 = pygame.Rect(635,370,85,85)
        self.patientRoomRect2 = pygame.Rect(720, 370, 95,85)
        self.patientRoomRect3 = pygame.Rect(815, 370, 85, 85)
        self.patientRoomRect4 = pygame.Rect(900, 370, 85,85)
        self.patientRoomRect5 = pygame.Rect(635, 455, 85,80)
        self.patientRoomRect6 = pygame.Rect(720, 455, 95,80)
        self.patientRoomRect7 = pygame.Rect(815, 455, 85,80)
        self.patientRoomRect8 = pygame.Rect(900, 455, 85,80)

        self.potionRoomRect = pygame.Rect(635, 280, 85,90)
        self.waitingRoomRect = pygame.Rect(720, 280, 95,90)
        self.garden1Rect = pygame.Rect(635, 535, 180, 75)
        self.garden2Rect = pygame.Rect(815, 535, 170, 75)

        self.otherRects = [
            self.potionRoomRect,
            self.waitingRoomRect,
            self.garden1Rect,
            self.garden2Rect
        ]

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

        for i, rect in enumerate(self.roomRects):
            # pygame.draw.rect(screen, (255,0,0), rect, 2)
            if GameData.roomData[i]["locked"] == False:
                textRenderer.render(screen, str(i+1), rect.center, 25, (255,255,255), align="center")
            else:
                screen.blit(self.lockImageShort, (rect.x-10, rect.y-10))
        
        textRenderer.render(screen, "Potion", (self.potionRoomRect.centerx, self.potionRoomRect.centery-10), 17, (255,255,255), align="center")
        textRenderer.render(screen, "Room", (self.potionRoomRect.centerx, self.potionRoomRect.centery+10), 17, (255,255,255), align="center")


        textRenderer.render(screen, "Waiting", (self.waitingRoomRect.centerx, self.waitingRoomRect.centery-10), 17, (255,255,255), align="center")
        textRenderer.render(screen, "Room", (self.waitingRoomRect.centerx, self.waitingRoomRect.centery+10), 17, (255,255,255), align="center")

        if GameData.gardenData["garden 1"]["locked"]:
            screen.blit(self.lockImageLong, (self.garden1Rect.x-10, self.garden1Rect.y-10))
        else:
            textRenderer.render(screen, "Garden 1", self.garden1Rect.center, 20, (255,255,255), align="center")

        if GameData.gardenData["garden 2"]["locked"]:
            screen.blit(self.lockImageLong,  (self.garden2Rect.x-10, self.garden2Rect.y-10))
        else:
            textRenderer.render(screen, "Garden 2", self.garden2Rect.center, 20, (255,255,255), align="center")
        
        # for rect in self.otherRects:
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
                    stateManager.queue[-1].mapIcon.isClosed = True
                
                for i in range(len(self.roomRects)):
                    if self.roomRects[i].collidepoint(pos):
                        if not GameData.roomData[i]["locked"]:
                            stateManager.push(PatientRoomState(i))

                if self.garden1Rect.collidepoint(pos) and not GameData.gardenData["garden 1"]["locked"]:
                    stateManager.push(Garden1())
                
                if self.garden2Rect.collidepoint(pos) and not GameData.gardenData["garden 2"]["locked"]:
                    stateManager.push(Garden2())
                
                if self.potionRoomRect.collidepoint(pos):
                    stateManager.push(PotionRoomState())
                
                if self.waitingRoomRect.collidepoint(pos):
                    stateManager.push(WaitingRoomState())

class PatientRoomState(State):
    def __init__(self, index):
        super().__init__()
        self.surface = pygame.Surface(orig_size)
        self.index = index
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds/VetMedicalRoom.png"), (orig_size[0], orig_size[1]))
        self.patient = GameData.patientsInRooms[self.index]
        self.shelf = pygame.transform.smoothscale_by(pygame.image.load("images/ui/MedicalRoomShelfButton.png"), .4)

        self.patient = GameData.patientsInRooms[self.index]
        self.inventoryButton = InventoryButton()
        self.downArrow = VerticalArrow(True)
        self.upArrow = VerticalArrow(False)
        self.leftArrow = Arrow(True)
        self.rightArrow = Arrow(False)
        self.mapIcon = MapButton()
        self.coins = Coins()
        self.settings = SettingsButton()
        self.uiElements = [self.leftArrow, self.rightArrow, self.downArrow, self.upArrow, self.mapIcon, self.coins, self.inventoryButton, self.settings]
        if self.index == len(GameData.roomData)-1:
            self.uiElements.remove(self.rightArrow)
        
        if self.index == 0:
            self.uiElements.remove(self.leftArrow)

    def render(self, screen, offset):
        super().render(screen, offset)
        self.surface.blit(self.background, (0,0))
        if self.patient != None:
            self.patient.render(self.surface)
        self.surface.blit(self.shelf, (120,150))
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
                    self.inventoryButton.closed = False
                    stateManager.push(InventoryOpenState())
                if self.leftArrow.checkClick():
                    if self.index > 0:
                        stateManager.transition(True)
                        stateManager.push(PatientRoomState(self.index-1))
                if self.rightArrow.checkClick():
                    if self.index < len(GameData.roomData)-1:
                        stateManager.transition(False)
                        stateManager.push(PatientRoomState(self.index+1))
                if self.downArrow.checkClick():
                    stateManager.transition(None, True)
                    stateManager.push(Garden1())
                if self.upArrow.checkClick():
                    stateManager.transition(None, False)
                    stateManager.push(WaitingRoomState())
                if self.mapIcon.checkClick():
                    self.mapIcon.isClosed = False
                    stateManager.push(MapState())
                if self.settings.checkClick():
                    stateManager.push(SettingsOpenState())

class InventoryOpenState(State):
    def __init__(self, currentTab=2, locked=False):
        super().__init__()
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/inventoryBackground.png"), .4)
        self.imageTop = pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/inventoryTop.png"), .4)
        self.imageBottom = pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/inventory_bg_bottom.png"), .4)
        self.pos = [400,100]
        self.surface = pygame.Surface((765,585), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.pos[0] + 65, self.pos[1] + 85, 740, 565)
        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(180)
        self.offset = 0
        self.rows = 5
        self.currentTab = currentTab
        self.locked = locked

        self.potionButton = InventoryStateRoundButton(
            pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/potionButton.png"), .078),
            [self.pos[0]+150, self.pos[1]+140], 60
        )
        self.ingredientButton = InventoryStateRoundButton(
            pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/ingredientButton.png"), .078),
            [self.pos[0]+320, self.pos[1]+140], 60
        )
        self.seedButton = InventoryStateRoundButton(
            pygame.transform.smoothscale_by(pygame.image.load("images/ui/inventory/seedButton.png"), .078),
            [self.pos[0]+490, self.pos[1]+140], 60
        )

        self.seedButton.isBig = True
        self.buttons = [self.potionButton, self.ingredientButton, self.seedButton]

        self.seeds = []
        for i, seed in enumerate(GameData.seedInventory):
            self.seeds.append(SeedItemInInventory(seed, (self.pos[0] + 90 + 110*(i%6), self.pos[1] + 240 + (i//6) * 110)))

        self.potions = []
        for i, potion in enumerate(GameData.potionsInInventory):
            self.potions.append(PotionItemInInventory(potion, (self.pos[0] + 90 + 110*(i%6), self.pos[1] + 240 + (i//6) * 110)))

        self.ingredients = []
        for i, ingredient in enumerate(GameData.ingredientsInInventory):
            self.ingredients.append(IngredientItemInInventory(ingredient, (self.pos[0] + 90 + 110*(i%6), self.pos[1] + 240 + (i//6) * 110)))

        self.itemLists = [self.potions, self.ingredients, self.seeds]

        self.scrollBar = ScrollBar(
            pygame.Rect(1160,350, 25, 360), 
            pygame.Rect(1165, 353, 15, 100), 
            (120,110,100), (160,140,130)
        )


    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.backgroundDark, (0,0))
        self.surface.blit(self.image, (-50,-75))
        for i in range(self.rows):
            for j in range(6):
                pygame.draw.rect(self.surface, (40,20,10), (45 + j*110, 185 + i*110 - self.offset, 95,95), 3, 5)

        for item in self.itemLists[self.currentTab]:
            item.render(self.surface, self.offset)
        
        self.surface.blit(self.imageTop, (-50,-75))
        self.surface.blit(self.imageBottom, (-50,-75))
        screen.blit(self.surface, (self.rect.x-15, self.rect.y-20))

        self.potionButton.render(screen)
        self.ingredientButton.render(screen)
        self.seedButton.render(screen)
        self.scrollBar.render(screen)
        


    def update(self):
        super().update()
        self.scrollBar.update()
        self.offset = self.scrollBar.offset


    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        self.scrollBar.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(pos):
                    stateManager.queue[-2].inventoryButton.closed = True
                    stateManager.pop()

                if not self.locked:
                    for i, button in enumerate(self.buttons):
                        if button.checkClick():
                            self.currentTab = i
                            for b in self.buttons:
                                b.isBig = False
                            button.isBig = True



class ForestState(State):
    def __init__(self):
        super().__init__()
        self.backgroundMain = pygame.transform.smoothscale_by(pygame.image.load("images/forest/layermain.png"), .35)
        self.backgroundLayer1 = pygame.transform.smoothscale_by(pygame.image.load("images/forest/layer1.png"), .35)
        self.backgroundLayer3 = pygame.transform.smoothscale_by(pygame.image.load("images/forest/layer2.png"), .35)
        self.backgroundLayer2 = pygame.transform.smoothscale_by(pygame.image.load("images/forest/layer3.png"), .35)
        self.posMain = [0,50]
        self.layer1Pos = [0,50]
        self.layer2Pos = [0,50]
        self.layer3Pos = [0,50]
        self.transitioningIn = True
        self.transitioningOut = False
        self.transitionScreen = pygame.Surface((WIDTH,HEIGHT))
        self.opacity = 255
        self.transitionSpeed = 10
        self.moveSpeed = 5

        self.goingLeft = False
        self.goingRight = False

        self.mapIcon = MapButton()
        self.coins = Coins()
        self.settings = SettingsButton()
        self.inventoryButton = InventoryButton()
        self.uiElements = [self.mapIcon, self.coins, self.inventoryButton, self.settings]
        

    def update(self):
        super().update()
        if self.transitioningIn:
            self.opacity -= self.transitionSpeed
            if self.opacity <= 0:
                self.transitioningIn = False
                self.opacity = 0
        if self.transitioningOut:
            self.opacity += self.transitionSpeed
            if self.opacity >= 255:
                self.opacity = 255
                self.transitioningOut = False

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.fill((255,255,255))
        screen.blit(self.backgroundMain, self.posMain)
        screen.blit(self.backgroundLayer1, self.layer1Pos)
        screen.blit(self.backgroundLayer2, self.layer2Pos)
        screen.blit(self.backgroundLayer3, self.layer3Pos)

        screen.blit(self.transitionScreen, (0,0))
        self.transitionScreen.set_alpha(self.opacity)

        if self.goingLeft:
            self.posMain[0] += self.moveSpeed
            self.layer1Pos[0] += self.moveSpeed * .8
            self.layer2Pos[0] += self.moveSpeed * .6
            self.layer3Pos[0] += self.moveSpeed * .4
        
        if self.goingRight:
            self.posMain[0] -= self.moveSpeed
            self.layer1Pos[0] -= self.moveSpeed * .8
            self.layer2Pos[0] -= self.moveSpeed * .6
            self.layer3Pos[0] -= self.moveSpeed * .4
        
        for element in self.uiElements:
            element.render(screen)

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        if not self.transitioningIn and not self.transitioningOut:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] < 100:
                        self.goingLeft = True
                    if pos[0] > 1200:
                        self.goingRight = True
                    if self.inventoryButton.checkClick():
                        self.inventoryButton.closed = False
                        stateManager.push(InventoryOpenState())
                    if self.mapIcon.checkClick():
                        self.mapIcon.isClosed = False
                        stateManager.push(MapState())
                    if self.settings.checkClick():
                        stateManager.push(SettingsOpenState())

                if event.type == pygame.MOUSEBUTTONUP:
                    self.goingLeft = False
                    self.goingRight = False


class PatientPopupState(State):
    def __init__(self, patient):
        super().__init__()
        self.background = pygame.Surface((500, 700))
        self.background.fill((220, 200, 180))
        self.rect = pygame.Rect(40, 40, 500, 700)
        self.patient = patient

        self.rects = []
        for i in range(8):
            self.rects.append(pygame.Rect(60 + (i % 4) * 60, 450 + (i // 4) * 60, 55, 55))

    def get_hover_rects(self):
        return self.rects


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


class DialogueState(State):
    def __init__(self, patient):
        super().__init__()
        self.patient = patient
        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(150)

        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/box.png"), .3)
        self.character = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/paige1.png"), .2)
        self.characterPos = [800,500]
        self.pos = [390,280]
        self.rect = pygame.Rect(645,640,640,260)
        self.dialogue = [self.get3LineDialogue(), self.get3LineDialogue(), self.get3LineDialogue()]
        self.dialogueTexts = []
        self.currentLine = 0
        self.currentChar = 0
        self.createDialogue()

        self.dialogueFinished = False
    
        pygame.time.set_timer(pygame.USEREVENT, 50)

    def createDialogue(self):
        self.dialogueTexts = []
        for l in range(len(self.dialogue)):
            temp = []
            for i in range(len(self.dialogue[l])):
                temp2 = []
                for j in range(len(self.dialogue[l][i])+1):
                    temp3 = []
                    k = 0
                    if i>0:
                        for _ in range(i):
                            temp3.append([self.dialogue[l][k], (700, 680+30*k)])
                            k += 1
                    temp3.append([self.dialogue[l][i][:j], (700, 680+30*k)])
                    temp2.append(temp3)
                temp.append(temp2)
            self.dialogueTexts.append(temp)

        temp = []
        for i in range(len(self.dialogueTexts)):
            temp2 = []
            for j in range(len(self.dialogueTexts[i])):
                for k in range(len(self.dialogueTexts[i][j])):
                    temp2.append(self.dialogueTexts[i][j][k])
            temp.append(temp2)

        self.dialogueTexts = temp



    def get3LineDialogue(self):
        text1 = random.choice(["My tummy hurts and I pooped the bed.", "My friends hurt my feelings.", "My poop is colorful.", "I burnt my snoot in my soup."])
        text2 = random.choice(["I'm also very itchy.", "I also can't stop sneezing.", "I also have been seeing things.", "I'm also very sad."])
        text3 = random.choice(["Help me!!!", "And my toes beans are stinky.", "And I miss my mommy."])
        return [text1, text2, text3]



    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.backgroundDark, (0,0))
        screen.blit(self.image, self.pos)
        screen.blit(self.character, self.characterPos)


        for i in range(len(self.dialogueTexts[self.currentLine][self.currentChar])):
            textRenderer.render(screen, self.dialogueTexts[self.currentLine][self.currentChar][i][0], self.dialogueTexts[self.currentLine][self.currentChar][i][1], 25, (20,10,2))



    def update(self):
        super().update()

    def handleInput(self, events):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.rect.collidepoint(pos):
                    stateManager.pop()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.currentChar < len(self.dialogueTexts[self.currentLine])-1:
                        self.currentChar = len(self.dialogueTexts[self.currentLine])-1
                    else:
                        if self.currentLine < len(self.dialogue)-1:
                            self.currentLine += 1
                            self.currentChar = 0
                        else:
                            self.dialogueFinished = True
                            stateManager.pop()
                            stateManager.push(RelocatePopupState(self.patient))

            if event.type == pygame.USEREVENT:
                if self.currentChar < len(self.dialogueTexts[self.currentLine]) - 1:
                    self.currentChar += 1



class RelocatePopupState(State):
    def __init__(self, patient):
        super().__init__()
        self.patient = patient
        self.backgroundDark = pygame.Surface((WIDTH, HEIGHT))
        self.backgroundDark.set_alpha(150)
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_.png"), .35)
        self.pos = [500,100]
        self.rect = pygame.Rect(510,115,580,510)
        self.roomButton = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_popup_button.png"), .35)
        self.uibutton = pygame.transform.smoothscale_by(pygame.image.load("images/dialogue/Dialogue_popup_button2.png"), .35)
        self.selectedButton = None

        self.sendToRoomRect = pygame.Rect(630, 575, 140, 40)
        self.cancelRect = pygame.Rect(840, 575, 140, 40)
        self.sentToRoom = False

    def render(self, screen, offset):
        super().render(screen, offset)
        screen.blit(self.backgroundDark, (0,0))
        screen.blit(self.image, self.pos)
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
                    stateManager.pop()
                if self.cancelRect.collidepoint(pos):
                    stateManager.pop()


