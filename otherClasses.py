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

        
