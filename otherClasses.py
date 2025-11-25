from patient import *




class Cauldron:
    def __init__(self, pos, scale=.5):
        self.animation = Animation("images/potionRoom/cauldronAnimation/", [
            "Untitled_Artwork-1.png", "Untitled_Artwork-2.png", "Untitled_Artwork-3.png", "Untitled_Artwork-4.png",
            "Untitled_Artwork-5.png", "Untitled_Artwork-6.png", "Untitled_Artwork-7.png", "Untitled_Artwork-8.png",
            "Untitled_Artwork-9.png", "Untitled_Artwork-10.png", "Untitled_Artwork-11.png", "Untitled_Artwork-12.png",
            "Untitled_Artwork-13.png", "Untitled_Artwork-14.png", "Untitled_Artwork-15.png", "Untitled_Artwork-16.png"
        ], 2, scale)
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
        self.pages = []
        page_index = 0
        for category_name, ingredients_dict in potionInfo["potion ingredients"].items():
            if category_name == "path":
                continue
            new_page = IngredientPage(category_name, ingredients_dict, page_index)
            self.pages.append(new_page)
            page_index += 1
        
        self.currentPageSet = 0

        if len(self.pages) > 0:
            self.max_page_sets = math.ceil(len(self.pages) / 2)
        else:
            self.max_page_sets = 1

        self.leftArrow = SmallArrow(True)
        self.rightArrow = SmallArrow(False)

    def render(self, screen):
        screen.blit(self.ingredientMenu, (10,10))
        screen.blit(self.ingredientMenu, (10,10))
        self.leftArrow.render(screen)
        self.rightArrow.render(screen)

        left_page_index = self.currentPageSet * 2
        right_page_index = left_page_index + 1

        if left_page_index < len(self.pages):
            self.pages[left_page_index].render(screen)
    
        if right_page_index < len(self.pages):
            self.pages[right_page_index].render(screen)

    def update(self):
        for page in self.pages:
            page.update()

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    self.currentPageSet -= 1
                    if self.currentPageSet < 0:
                        self.currentPageSet = self.max_page_sets - 1
                        
                if self.rightArrow.checkClick():
                    self.currentPageSet += 1
                    if self.currentPageSet >= self.max_page_sets:
                        self.currentPageSet = 0


class IngredientPage:
    def __init__(self, category_name, ingredients_dict, page_index):
        self.ingredients = []
        self.title = category_name
        
        self.is_on_right_side = (page_index % 2 == 1)

        item_index = 0
        for ingredient_name, ingredient_data in ingredients_dict.items():
            ingredient = PotionIngredient(
                name=ingredient_name,
                category=category_name,
                pos=[160 + (item_index % 6) * 70, 170 + (item_index // 6) * 45],
                quantity=ingredient_data["quantity"],
                scale=ingredient_data["scale"],
                is_on_right_side = self.is_on_right_side
            )
            self.ingredients.append(ingredient)
            item_index += 1

    def render(self, screen):
        if self.is_on_right_side:
            textRenderer.render(screen, self.title.capitalize(), (1140, 100), 30, (255,255,255), align="center")
        else:
            textRenderer.render(screen, self.title.capitalize(), (420,100), 30, (255,255,255), align="center")
            
        for item in self.ingredients:
            item.render(screen)

    def update(self):
        for ingredient in self.ingredients:
            ingredient.update()

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass


class PotionIngredient:
    def __init__(self, name, category, pos, quantity, scale, is_on_right_side=False):
        path = potionInfo["potion ingredients"]["path"] + potionInfo["potion ingredients"][category][name]["path"]
        self.image = pygame.transform.scale_by(pygame.image.load(path).convert_alpha(), scale)
        self.faintImage = self.image.copy()
        self.faintImage.set_alpha(60)
        self.name = name
        self.category = category
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        
        if is_on_right_side:
            self.pos[0] += 730
            self.rect.x += 730
        
        self.quantity = quantity

    def render(self, screen):
        if self.quantity == 0:
            screen.blit(self.faintImage, self.pos)
        if self.quantity > 0:
            self.image.set_alpha(1000)
            screen.blit(self.image, self.pos)
        textRenderer.render(screen, str(self.quantity), (self.pos[0]+30, self.pos[1]+30), 20, (255,255,255))

    def update(self):
        if self.quantity < 1:
            self.image.set_alpha(60)

    def handleInput(self, events):
        pass

    def checkClick(self):
        pos = pygame.mouse.get_pos()
        clicked = self.rect.collidepoint(pos[0], pos[1])
        return clicked
    


class PotionIngredientDragging:
    def __init__(self, image, category, name, offset):
        self.scale = 2
        self.image = pygame.transform.scale_by(image, self.scale)
        self.image.set_alpha(1000)
        self.offset = offset
        self.name = name
        self.category = category

    def render(self, screen):
        pos = pygame.mouse.get_pos()
        screen.blit(self.image, [pos[0]-self.offset[0], pos[1]-self.offset[1]])


class PotionIngredientInCauldron:
    def __init__(self, image, category, name, startPos, endPos):
        self.scale = .8
        self.fallingImage = image
        self.fallingImage.set_alpha(1000)
        self.image = pygame.transform.scale_by(image, self.scale)
        self.image.set_alpha(1000)
        self.name = name
        self.category = category
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
        # textRenderer.render(screen, str(self.quantity), (self.endPos[0]+60, self.endPos[1]+60), 20, (255,255,255))

        

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
        
        # --- Image Loading (Unchanged) ---
        # NOTE: You must ensure these files exist for Pygame to run.
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
        
        
        # New plant initialized
        self.currentState = 0
        self.plantTime = datetime.now() # Record the real-world time it was planted
        self.pos = [position, 650]
        print(f"Initialized new {self.plantName}.")
            
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
        """Draws the current plant stage and dirt."""
        # Adjust height based on current image size
        plant_y = self.pos[1] - self.currentImg.get_height()
        screen.blit(self.currentImg, [self.pos[0], plant_y])
        
        # Dirt drawn slightly lower
        dirt_y = self.pos[1] - self.dirt.get_height()
        screen.blit(self.dirt, [self.pos[0], dirt_y])

    def update(self):
        """Checks real-world time and advances the plant's stage if time elapsed."""
        
        # The plant is fully grown and no longer needs updates
        if self.currentState >= len(self.imgs) - 1:
            return 
        
        current_real_time = datetime.now()
        
        # Calculate the time elapsed since the last stage transition
        time_elapsed = current_real_time - self.plantTime
        
        # Get the required time (in the defined unit) for the current stage transition
        # self.currentState maps to the required time index in growTime
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
            
        
        # Check if the elapsed real-world time meets or exceeds the required duration
        if time_elapsed >= required_duration:
            # Advance to the next stage
            self.currentState += 1
            self.currentImg = self.imgs[self.currentState]
            
            # Reset the stage timer to NOW. This is crucial!
            # The next transition will be measured from this new time.
            self.plantTime = current_real_time 
            
            print(f"[{current_real_time.strftime('%H:%M:%S')}] {self.plantName} Grew to Stage {self.currentState}!")
            
            if self.currentState >= len(self.imgs) - 1:
                print(f"{self.plantName} is now fully grown!")

        else:
            # Optional: Display time remaining for debugging/UI purposes
            time_remaining = required_duration - time_elapsed
            # print(f"Stage {self.currentState}: {time_remaining} remaining.")
            pass