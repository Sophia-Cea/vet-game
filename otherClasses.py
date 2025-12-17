from patient import *




class Cauldron:
    def __init__(self, pos, scale=.5):
        self.animation = Animation("images/potionRoom/cauldronAnimation/", [
            "Cauldron_F1.png", "Cauldron_F2.png", "Cauldron_F3.png", "Cauldron_F4.png",
            "Cauldron_F5.png", "Cauldron_F6.png", "Cauldron_F7.png", "Cauldron_F8.png",
            "Cauldron_F9.png", "Cauldron_F10.png", "Cauldron_F11.png"
        ], 1.83, scale)
        self.pos = pos
        self.rect = pygame.Rect(pos[0]+160,pos[1]+190,200,200)
        self.textcol = (67, 40, 24)

    def render(self, screen):
        self.animation.render(screen, self.pos)

    def update(self):
        self.animation.update()
    
    def checkClick(self):
        pos = pygame.mouse.get_pos()
        clicked = self.rect.collidepoint(pos[0], pos[1])
        return clicked



class PotionIngredientMenu:
    def __init__(self):
        self.ingredientMenu = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/ui/potioningredientsui.png"), .4)
        self.rect1 = pygame.Rect(135,130, 570,205)
        self.rect2 = pygame.Rect(860,130, 570,205)

        self.leftSurf = pygame.Surface((570,205))
        self.rightSurf = pygame.Surface((570,205))
        self.scrollLeft = ScrollBar(pygame.Rect(680,140, 20, 180), pygame.Rect(683,143, 14, 60), (153, 88, 42), (255, 230, 167))
        self.scrollRight = ScrollBar(pygame.Rect(1400,140, 20, 180), pygame.Rect(1403,143, 14, 60), (153, 88, 42), (255, 230, 167))
        self.offsetLeft = 0
        self.offsetRight = 0

        self.ingredients = []
        self.potions = []

        for i, ingredient in enumerate(GameData.ingredientsInInventory):
            self.ingredients.append(IngredientItemInPotionInventory(ingredient, (35 + (i%5) * 95, 20 + (i//5) * 95)))\
            
        for i, potion in enumerate(GameData.potionsInInventory):
            self.potions.append(PotionItemInPotionInventory(potion, (35 + (i%5) * 95, 20 + (i//5) * 95)))

        self.draggingItem = None

    

    def render(self, screen):
        screen.blit(self.ingredientMenu, (10,-20))
        screen.blit(self.ingredientMenu, (10,-20))
        textRenderer.render(screen, "Ingredients", (420, 70), 35, (250,230,210), align="center")
        textRenderer.render(screen, "Potions", (1140, 70), 35, (250,230,210), align="center")

        self.leftSurf.fill((74, 38, 35))
        self.rightSurf.fill((74, 38, 35))

        for i in range(4): 
            for j in range(5): 
                pygame.draw.rect(self.leftSurf, (187, 148, 87), (35+j*95, 20+i*95-self.offsetLeft, 80,80), 3, 4)

        for i in range(4):
            for j in range(5):
                pygame.draw.rect(self.rightSurf, (187, 148, 87), (35+j*95, 20+i*95-self.offsetRight, 80,80), 3, 4)

        for item in self.ingredients:
            item.render(self.leftSurf, self.offsetLeft)

        for item in self.potions:
            item.render(self.rightSurf, self.offsetRight)


        screen.blit(self.leftSurf, self.rect1.topleft)
        screen.blit(self.rightSurf, self.rect2.topleft)

        self.scrollLeft.render(screen)
        self.scrollRight.render(screen)


    def update(self):
        self.scrollLeft.update()
        self.scrollRight.update()
        self.offsetLeft = self.scrollLeft.offset * 2
        self.offsetRight = self.scrollRight.offset * 2


    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        self.scrollLeft.handleInput(events)
        self.scrollRight.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for ingredient in self.ingredients:
                    rect = pygame.Rect(ingredient.rect.x + self.rect1.x, ingredient.rect.y + self.rect1.y - self.offsetLeft, ingredient.rect.w, ingredient.rect.h)
                    if rect.collidepoint(pos):
                        offset = [pos[0] - rect.x, pos[1] - rect.y]
                        self.draggingItem = PotionIngredientDragging(ingredient.image, ingredient.name, offset)

            if event.type == pygame.MOUSEBUTTONUP:
                self.draggingItem = None












class PotionIngredientDragging:
    def __init__(self, image, name, offset):
        self.scale = 2
        self.image = pygame.transform.scale_by(image, self.scale)
        self.image.set_alpha(1000)
        self.offset = offset
        self.name = name

    def render(self, screen):
        pos = pygame.mouse.get_pos()
        screen.blit(self.image, [pos[0]-self.offset[0], pos[1]-self.offset[1]])


class PotionIngredientInCauldron:
    def __init__(self, image, name, startPos, endPos):
        self.scale = .8
        self.fallingImage = image
        self.fallingImage.set_alpha(1000)
        self.image = pygame.transform.scale_by(image, self.scale)
        self.image.set_alpha(1000)
        self.name = name
        self.startPos = [startPos[0], startPos[1]]
        self.endPos = [endPos[0], endPos[1]]
        self.falling = True
        self.quantity = 1

        self.acceleration = 1.5
        self.velocity = 1

    def render(self, screen):
        if self.falling:
            self.startPos[1] += self.velocity
            self.velocity += self.acceleration
            if self.startPos[1] > 650:
                self.falling = False
            screen.blit(self.fallingImage, self.startPos)
    
        screen.blit(self.image, self.endPos)




GROW_TIME_UNIT = "minutes" # Set to minutes for easy testing!


class GardenPlant:
    """
    Represents a plant that grows over real-world time.
    Persistence requires saving and loading: currentState, plantTime, and pos.
    """
    def __init__(self, plantName, position):
        self.plantName = plantName
        self.plantData = plantInfo[plantName]
        self.path = self.plantData["path"]
        try:
            self.imgs = [
                pygame.transform.smoothscale_by(pygame.image.load(self.path + self.plantData["seed"]), .25)
            ]
            for img in self.plantData["in betweens"]:
                self.imgs.append(pygame.transform.smoothscale_by(pygame.image.load(self.path + img), .25))
            self.imgs.append(pygame.transform.smoothscale_by(pygame.image.load(self.path + self.plantData["fullgrown"]), .25))
            self.dirt = pygame.transform.smoothscale_by(pygame.image.load("images/garden/dirt.png"), .25)
        except pygame.error as e:
            print(f"Error loading images for {plantName}. Ensure files exist in '{self.path}': {e}")
            # Use placeholders if images fail to load
            self.imgs = [pygame.Surface((100, 100)) for _ in range(len(self.plantData["in betweens"]) + 2)]
            self.dirt = pygame.Surface((100, 50))
        # -----------------------------------
        
        self.fullyGrown = False
        self.currentState = 0
        self.plantTime = datetime.now() # Record the real-world time it was planted
        self.pos = [position, 850] # plants position
            
        self.currentImg = self.imgs[self.currentState]

    def get_save_data(self):
        """Returns a dict ready to be JSON serialized."""
        return {
            "plantName": self.plantName,
            "currentState": self.currentState,
            # datetime must be converted to an ISO string for saving
            "plantTime": self.plantTime.isoformat(), 
            "pos": self.pos
        }

    def render(self, screen):
        plant_y = self.pos[1] - self.currentImg.get_height()
        screen.blit(self.currentImg, [self.pos[0], plant_y])
        dirt_y = self.pos[1] - self.dirt.get_height()
        screen.blit(self.dirt, [self.pos[0], dirt_y])

    def update(self):
        # The plant is fully grown and no longer needs updates
        if self.currentState >= len(self.imgs) - 1:
            return 
        
        current_real_time = datetime.now()
        time_elapsed = current_real_time - self.plantTime
        required_unit_value = self.plantData["growTime"][self.currentState]
        
        # Convert the required value into a timedelta object for comparison
        if GROW_TIME_UNIT == "minutes":
            required_duration = timedelta(minutes=required_unit_value)
        elif GROW_TIME_UNIT == "hours":
            required_duration = timedelta(hours=required_unit_value)
        elif GROW_TIME_UNIT == "days":
            required_duration = timedelta(days=required_unit_value)
        else: # Default to seconds if unit is unknown or seconds
            required_duration = timedelta(seconds=required_unit_value)
            
        
        if time_elapsed >= required_duration:
            self.currentState += 1
            self.currentImg = self.imgs[self.currentState]
            
            self.plantTime = current_real_time 
            
            if self.currentState >= len(self.imgs) - 1:
                self.fullyGrown = True

        else:
            # Optional: Display time remaining for debugging/UI purposes
            time_remaining = required_duration - time_elapsed
            # print(f"Stage {self.currentState}: {time_remaining} remaining.")
            pass


class HoneyCombItem:
    def __init__(self):
        self.honeycombImage = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/potionIngredients/honeycomb.png"), .05)
        self.honeycombPos = [1080,290]
        self.rect = pygame.Rect(1100,580,65,50)
        self.dropping = False
        self.dropped = False
        self.veloc = 0
        self.accel = .7
        self.finalPos = 550
        self.bounced = False
        self.waitTime = 5 # seconds
        self.pickUp = None
        self.dropTime = None
    
    def render(self, screen):
        if self.dropping or self.dropped:
            screen.blit(self.honeycombImage, self.honeycombPos)

    def update(self):
        if self.dropping:
            self.honeycombPos[1] += self.veloc
            self.veloc += self.accel
            if self.honeycombPos[1] >= self.finalPos:
                if self.bounced:
                    self.dropped = True
                    self.dropTime = datetime.now()
                    self.dropping = False
                if not self.bounced:
                    self.bounced = True
                    self.veloc = -5

        if self.dropped:
            current_real_time = datetime.now()
            time_elapsed = current_real_time - self.dropTime

            required_duration = timedelta(seconds=self.waitTime)
            if time_elapsed >= required_duration:
                self.pickUp = True

    def handleInput(self, events):
        for event in events:
            pass

    def drop(self):
        self.dropping = True


class Beehive:
    def __init__(self):
        self.pos = [1050,250]
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/garden/beehive.png"), .1)
        self.honey = pygame.transform.smoothscale_by(pygame.image.load("images/garden/honey-splatters.png"), .1)
        self.isReady = False
        self.honeyTime = 10 # seconds
        self.rect = pygame.Rect(1100,280,95,125)
        self.harvestHoney = False
        self.harvestTime = datetime.now()
        self.honeycomb = HoneyCombItem()
        self.dropping = False

    def resetHoneyComb(self):
        self.honeycomb = HoneyCombItem()

    def render(self, screen):
        screen.blit(self.image, self.pos)
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        if self.isReady:
            screen.blit(self.honey, self.pos)
        self.honeycomb.render(screen)

    
    def update(self):
        self.honeycomb.update()

        if self.honeycomb.pickUp:
            self.addToInventory()
            self.resetHoneyComb()
    

        if self.isReady:
            return
        
        current_real_time = datetime.now()
        time_elapsed = current_real_time - self.harvestTime

        required_duration = timedelta(seconds=self.honeyTime)
        if time_elapsed >= required_duration:
            self.isReady = True
        
        
    def addToInventory(self):
        itemAdded = False
        for i, item in enumerate(GameData.ingredientsInInventory):
            if item["name"] == "Honeycomb":
                GameData.ingredientsInInventory[i]["quantity"] += 1
                itemAdded = True
        if not itemAdded:
            GameData.ingredientsInInventory.append(
                {
                    "name": "Honeycomb",
                    "quantity" : 1
                }
            )



    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        self.honeycomb.handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(pos) and self.isReady:
                    self.harvestHoney = True
                    self.isReady = False
                    self.harvestTime = datetime.now()
                    self.honeycomb.drop()
                if self.honeycomb.dropped and self.honeycomb.rect.collidepoint(pos):
                    self.addToInventory()
                    self.resetHoneyComb()

