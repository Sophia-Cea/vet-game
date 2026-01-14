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


class GardenPlot:
    def __init__(self, plantIndex):
        self.plantIndex = plantIndex
        self.plant = GameData.gardenData["plots"][self.plantIndex]["plant"]
        self.dirt = pygame.transform.smoothscale_by(pygame.image.load("images/garden/dirt.png"), .25)
        self.pos = GameData.gardenData["plots"][self.plantIndex]["pos"]
        self.rect = pygame.Rect(self.pos[0]-40, self.pos[1]+100, 180, 80)

        self.diggingUp = False
        self.planting = False

        self.progressBar = pygame.Surface((108,14), pygame.SRCALPHA)
        self.progress = 0
        self.offset = 0
        self.plantItem = None
        self.droppingItem = False


    def calculateProgress(self):
        if self.plant is None:
            self.progress = 0
            return

        # 1. Get the TOTAL time required (Denominator)
        # Sum of all stages in the list
        total_duration = sum(self.plant.plantData["growTime"]) 
        
        # 2. Get the time passed in COMPLETED stages
        time_from_completed_stages = 0
        for i in range(self.plant.currentState):
            # Ensure we don't go out of bounds if currentState exceeds list length
            if i < len(self.plant.plantData["growTime"]):
                time_from_completed_stages += self.plant.plantData["growTime"][i]
        
        # 3. Get the time passed in the CURRENT stage
        time_from_current_stage = 0
        if self.plant.time_elapsed is not None:
            # Convert timedelta to minutes to match your growTime data
            # (Assuming growTime is in minutes because you divided by 60 previously)
            time_from_current_stage = self.plant.time_elapsed.total_seconds() / 60
            
        # 4. Combine numerator: (Past Time + Current Time)
        total_time_passed = time_from_completed_stages + time_from_current_stage

        # 5. Calculate Final Percentage
        if total_duration > 0:
            self.progress = (total_time_passed / total_duration) * 100
        else:
            self.progress = 100
            
        # Clamp to 100 to prevent visual overflow
        if self.progress > 100:
            self.progress = 100
            
            
    def render(self, screen, offset):
        self.offset = offset

        if self.plant != None:
            self.plant.render(screen, offset)

        screen.blit(self.dirt, (self.pos[0]-50+offset, self.pos[1]-30))

        if self.plant != None and self.plant.harvesting == False:
            pygame.draw.rect(self.progressBar, (200,190,170), (0,0, 108, 14), 0, 6) # background color
            pygame.draw.rect(self.progressBar, (120,90,20), (4,0, self.progress, 14)) # progress bar
            pygame.draw.rect(self.progressBar, (80,50,20), (0,0,108,14), 4, 6) # border

            screen.blit(self.progressBar, (self.rect.x + 25+offset, self.rect.y + 35))

        if self.droppingItem:
            self.plantItem.render(screen, offset)
        
        elif self.plant == None:
            screen.blit(self.dirt, (self.pos[0]-50+offset, self.pos[1]-30))

    def update(self):
        if self.plant != None:
            self.plant.update()
        
        if self.droppingItem == True:
            self.plantItem.update()
        
        self.calculateProgress()


    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(self.rect.x+self.offset, self.rect.y, self.rect.w, self.rect.h).collidepoint(pos):
                    if self.plant != None:
                        self.diggingUp = True
                    elif self.plant == None:
                        self.planting = True


                if self.plant != None:
                    if self.plant.fullyGrown:
                        if pygame.Rect(self.plant.rect.x+self.offset, self.plant.rect.y, self.plant.rect.w, self.plant.rect.h).collidepoint(pos):
                            if self.plantItem != None:
                                # make it pick up whatever was there first so it doesnt go to waste
                                self.plantItem = None
                            if self.plantItem == None:
                                self.plantItem = PlantItemDrop(self.plant.plantName, self.plant.path + self.plant.plantData["item image"], self.plant.rect)
                            self.plant = None
                            GameData.gardenData["plots"][self.plantIndex]["plant"] = None
                            self.droppingItem = True

                if self.plantItem != None and self.plantItem.readyForCollecting == True:
                    if pygame.Rect(self.plantItem.rect.x+self.offset, self.plantItem.rect.y, self.plantItem.rect.w, self.plantItem.rect.h).collidepoint(pos):
                        self.plantItem = None
                        self.droppingItem = False
                        # make sure to add item to inventory



class GardenPlant:
    """
    Represents a plant that grows over real-world time.
    Persistence requires saving and loading: currentState, plantTime, and pos.
    """
    def __init__(self, plantName, pos):
        self.plantName = plantName
        self.plantData = plantInfo[plantName]
        self.path = self.plantData["path"]
        self.imgs = [
            pygame.transform.smoothscale_by(pygame.image.load(self.path + self.plantData["seed"]), .25)
        ]
        for img in self.plantData["in betweens"]:
            self.imgs.append(pygame.transform.smoothscale_by(pygame.image.load(self.path + img), .25))
        self.imgs.append(pygame.transform.smoothscale_by(pygame.image.load(self.path + self.plantData["fullgrown"]), .25))
        
        
        self.fullyGrown = False
        self.currentState = 0
        self.plantTime = datetime.now() # Record the real-world time it was planted
        self.pos = [pos[0]-20, pos[1]+175] # plants position
        self.currentImg = self.imgs[self.currentState]
        self.time_elapsed = None
        self.required_duration = None

        size = plantInfo[self.plantName]["size"]
        self.plantOffset = plantInfo[self.plantName]["offset"]
        self.rect = pygame.Rect(self.pos[0]+10, self.pos[1]-size[1]-30, size[0], size[1])
        self.harvesting = False

    def get_save_data(self):
        """Returns a dict ready to be JSON serialized."""
        return {
            "plantName": self.plantName,
            "currentState": self.currentState,
            # datetime must be converted to an ISO string for saving
            "plantTime": self.plantTime.isoformat(), 
            "pos": self.pos
        }

    def render(self, screen, offset):
        if not self.harvesting:
            plant_y = self.pos[1] - self.currentImg.get_height()
            if self.currentState > 0:
                screen.blit(self.currentImg, [self.pos[0]+offset+self.plantOffset[0], plant_y+self.plantOffset[1]])
            else:
                screen.blit(self.currentImg, [self.pos[0]+offset, plant_y])

            if plantInfo[self.plantName]["testing"] == True:
                pygame.draw.rect(screen, (255,0,0), self.rect, 2)
            
        
    def update(self):
        if not self.harvesting and not self.fullyGrown:
            current_real_time = datetime.now()
            time_elapsed = current_real_time - self.plantTime
            required_unit_value = self.plantData["growTime"][self.currentState]
            
            # Convert the required value into a timedelta object
            if GROW_TIME_UNIT == "minutes":
                required_duration = timedelta(minutes=required_unit_value)
            elif GROW_TIME_UNIT == "hours":
                required_duration = timedelta(hours=required_unit_value)
            elif GROW_TIME_UNIT == "days":
                required_duration = timedelta(days=required_unit_value)
            else: 
                required_duration = timedelta(seconds=required_unit_value)
                
            self.time_elapsed = time_elapsed
            self.required_duration = required_duration

            if time_elapsed >= required_duration:
                self.currentState += 1
                self.currentImg = self.imgs[self.currentState]
                
                self.plantTime = current_real_time 
                
                self.time_elapsed = timedelta(0) 

                if self.currentState >= len(self.imgs) - 1:
                    self.fullyGrown = True



class PlantItemDrop:
    def __init__(self, plantName, path, plantRect):
        self.plantName = plantName
        self.image = pygame.transform.smoothscale_by(pygame.image.load(path), .09)
        self.horizontalVelocity = random.randint(-3,3)
        self.verticalVelocity = random.randint(-10,-6)
        self.verticalStartPoint = plantRect.y + random.randint(10, int(plantRect.h/3))
        self.verticalEndPoint = max(self.verticalStartPoint + random.randint(80,100), 530)
        self.bounced = False
        self.acceleration = 0.8
        self.postBounceVelocity = random.randint(-8,-5)
        self.rect = None
        self.pos = [plantRect.x+plantRect.w/2-20, self.verticalStartPoint]
        self.readyForCollecting = False


    def render(self, screen, offset):
        screen.blit(self.image, (self.pos[0] + offset, self.pos[1]))
        if self.readyForCollecting:
            pygame.draw.rect(screen, (255,0,0), self.rect, 2)


    def update(self):
        if not self.bounced:
            self.pos[1] = self.pos[1] + self.verticalVelocity
            self.pos[0] += self.horizontalVelocity
            self.verticalVelocity += self.acceleration
            if self.pos[1] >= self.verticalEndPoint:
                self.pos[1] = self.verticalEndPoint
                self.bounced = True
                self.verticalVelocity = self.postBounceVelocity
        else:
            if not self.readyForCollecting:
                self.pos[1] = self.pos[1] + self.verticalVelocity
                self.pos[0] += self.horizontalVelocity
                self.verticalVelocity += self.acceleration
                if self.pos[1] >= self.verticalEndPoint:
                    self.readyForCollecting = True
                    self.rect = pygame.Rect(self.pos[0], self.pos[1], 50,50)

    def handleInput(self):
        pass




class HoneyCombItem:
    def __init__(self):
        self.honeycombImage = pygame.transform.smoothscale_by(pygame.image.load("images/potionRoom/potionIngredients/honeycomb.png"), .05)
        self.honeycombPos = [2500,290]
        self.rect = pygame.Rect(2510,540,65,50)
        self.dropping = False
        self.dropped = False
        self.veloc = 0
        self.accel = .9
        self.finalPos = 540
        self.bounced = False
        self.waitTime = 5 # seconds
        self.pickUp = None
        self.dropTime = None
        self.offset = 0
    
    def render(self, screen, offset):
        self.offset = offset
        if self.dropping or self.dropped:
            screen.blit(self.honeycombImage, (self.honeycombPos[0] + offset, self.honeycombPos[1]))
            # pygame.draw.rect(screen, (255,0,0), (self.rect.x+offset, self.rect.y, self.rect.w, self.rect.h), 2)

    def update(self):
        if self.dropping:
            self.honeycombPos[1] += self.veloc
            if self.honeycombPos[1] > self.finalPos:
                self.honeycombPos[1] = self.finalPos
            self.veloc += self.accel
            if self.honeycombPos[1] >= self.finalPos:
                if self.bounced:
                    self.dropped = True
                    GameData.currentData["honey data"]["readyForPickup"] = True
                    self.dropTime = datetime.now()
                    self.dropping = False
                if not self.bounced:
                    self.bounced = True
                    self.veloc = -8

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
        self.pos = [2470,225]
        self.image = pygame.transform.smoothscale_by(pygame.image.load("images/garden/beehive.png"), .1)
        self.honey = pygame.transform.smoothscale_by(pygame.image.load("images/garden/honey-splatters.png"), .1)
        # self.isReady = False
        self.honeyTime = 10 # seconds
        self.rect = pygame.Rect(2515,255,105,125)
        self.harvestedHoney = GameData.currentData["honey data"]["readyForHarvest"]
        self.harvestTime = GameData.currentData["honey data"]["lastHoneyHarvest"]
        self.honeycomb = HoneyCombItem()
        self.offset = 0

    def resetHoneyComb(self):
        self.honeycomb = HoneyCombItem()

    def render(self, screen, offset):
        self.offset = offset
        screen.blit(self.image, (self.pos[0] + offset, self.pos[1]))
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        if GameData.currentData["honey data"]["readyForHarvest"]== True:
            screen.blit(self.honey, (self.pos[0] + offset, self.pos[1]))
        self.honeycomb.render(screen, offset)

        # pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.rect.x + self.offset, self.rect.y, self.rect.w, self.rect.h), 2)

    
    def update(self):
        self.honeycomb.update()

        if self.honeycomb.pickUp:
            self.addToInventory()
            self.resetHoneyComb()
            GameData.currentData["honey data"]["ready for reset"] = True
    
        
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
                if pygame.Rect(self.rect.x + self.offset, self.rect.y, self.rect.w, self.rect.h).collidepoint(pos) and GameData.currentData["honey data"]["readyForHarvest"] == True:
                    print("clicked")
                    self.harvestedHoney = True
                    GameData.currentData["honey data"]["readyForHarvest"] = False
                    self.harvestTime = datetime.now()
                    GameData.currentData["honey data"]["lastHoneyHarvest"] = datetime.now()
                    self.honeycomb.drop()

                if self.honeycomb.dropped and pygame.Rect(self.honeycomb.rect.x + self.offset, self.honeycomb.rect.y, self.honeycomb.rect.w, self.honeycomb.rect.h).collidepoint(pos):
                    GameData.currentData["honey data"]["ready for reset"] = True
                    self.addToInventory()
                    self.resetHoneyComb()



class Cloud:
    def __init__(self):
        self.image = random.choice([
            pygame.image.load("images/garden/cloud-1.png"),
            pygame.image.load("images/garden/cloud-2.png"),
            pygame.image.load("images/garden/cloud-3.png"),
            pygame.image.load("images/garden/cloud-4.png")
        ])
        self.image = pygame.transform.smoothscale_by(self.image, .25)
        self.speed = random.randint(4,12)/5
        self.pos = [random.randint(3000,5000), random.randint(-200, 0)]
        self.finished = False

    def render(self, screen, offset):
        screen.blit(self.image, (self.pos[0]+offset, self.pos[1]))

    def update(self):
        self.pos[0] -= self.speed
        if self.pos[0] < -400:
            self.finished = True

    def handleInput(self, events):
        pass

class Raincloud:
    def __init__(self):
        self.image = random.choice([
            pygame.image.load("images/garden/raincloud-1.png"),
            pygame.image.load("images/garden/raincloud-2.png"),
            pygame.image.load("images/garden/raincloud-3.png"),
            pygame.image.load("images/garden/raincloud-4.png")
        ])
        self.image = pygame.transform.smoothscale_by(self.image, .25)
        self.speed = random.randint(4,12)/5
        self.pos = [3000,random.randint(150, 400)]
        self.finished = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 300, 100)

    def render(self, screen, offset):
        screen.blit(self.image, (self.pos[0]+offset, self.pos[1]))

    def update(self):
        self.pos[0] -= self.speed
        self.rect.x -= self.speed
        if self.pos[0] < -400:
            self.finished = True

    def handleInput(self, events):
        pass




class GardenSky:
    def __init__(self):
        self.clouds = []
        self.rainClouds = []
        self.raining = False
        self.rainstormDuration = None
        self.rainstormStart = None

        for i in range(10):
            self.clouds.append(Cloud())

    def render(self, screen, offset):
        for cloud in self.clouds:
            cloud.render(screen, offset)

        for cloud in self.rainClouds:
            cloud.render(screen, offset)


    def update(self):
        for cloud in self.clouds:
            cloud.update()
            if cloud.finished == True:
                self.clouds.remove(cloud)
                if self.raining == False:
                    self.clouds.append(Cloud())
        
        for cloud in self.rainClouds:
            cloud.update()
            if cloud.finished == True:
                self.rainClouds.remove(cloud)
                if self.raining == True:
                    self.rainClouds.append(Raincloud())

            
            if len(self.rainClouds) == 0:
                for i in range(10):
                    self.rainClouds.append(Raincloud())
        
        if not self.raining and len(self.clouds) < 10:
            self.clouds.append(Cloud())
            
        


    def handleInput(self, events):
        for cloud in self.clouds:
            cloud.handleInput(events)
        
        for cloud in self.rainClouds:
            cloud.handleInput(events)