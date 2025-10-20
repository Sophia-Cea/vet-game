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
        
        # Calculate the total number of page "sets" we can flip through.
        # For example, 5 pages would be 3 sets: (page 0,1), (page 2,3), and (page 4, empty)
        # We use ceiling division to make sure we account for the last partial set.
        if len(self.pages) > 0:
            self.max_page_sets = math.ceil(len(self.pages) / 2)
        else:
            self.max_page_sets = 1 # Avoid division by zero if there are no pages

        self.leftArrow = SmallArrow(True)
        self.rightArrow = SmallArrow(False)

    def render(self, screen):
        # Your original code blitted this twice. You might only need one.
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
        pass

    def handleInput(self, events):
        for event in events:
            # We only care about the mouse button being released.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftArrow.checkClick():
                    print("was clicked left")
                    # Go to the previous page set
                    self.currentPageSet -= 1
                    # If we go past the first page, wrap around to the last page.
                    if self.currentPageSet < 0:
                        self.currentPageSet = self.max_page_sets - 1
                        
                if self.rightArrow.checkClick():
                    print("was clicked right")
                    # Go to the next page set
                    self.currentPageSet += 1
                    # If we go past the last page, wrap around to the first page.
                    if self.currentPageSet >= self.max_page_sets:
                        self.currentPageSet = 0



# --- IngredientPage Class ---
# This class now handles everything for a single category.

class IngredientPage:
    def __init__(self, category_name, ingredients_dict, page_index):
        self.ingredients = []
        self.title = category_name
        
        # Determines if this page's ingredients should be drawn on the right panel.
        # In your original code, the 'leftSide' parameter actually moved items to the right.
        self.is_on_right_side = (page_index % 2 == 1)

        # The logic to create PotionIngredient objects now lives here.
        item_index = 0
        for ingredient_name, ingredient_data in ingredients_dict.items():
            ingredient = PotionIngredient(
                name=ingredient_name,
                category=category_name,
                # This calculates the grid position within the panel.
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
        # The page tells each of its ingredients to draw itself.
        for item in self.ingredients:
            item.render(screen)

    def update(self):
        pass

    def handleInput(self, events):
        pass

# --- PotionIngredient Class ---
# This class is mostly unchanged, but I've renamed a parameter for clarity.

class PotionIngredient:
    def __init__(self, name, category, pos, quantity, scale, is_on_right_side=False):
        path = potionInfo["potion ingredients"]["path"] + potionInfo["potion ingredients"][category][name]["path"]
        self.image = pygame.transform.scale_by(pygame.image.load(path).convert_alpha(), scale)
        self.pos = pos
        
        # If this ingredient belongs to a right-side page, offset its x position.
        if is_on_right_side:
            self.pos[0] += 730
            
        self.quantity = quantity
        if self.quantity == 0:
            self.image.set_alpha(60) # Make it semi-transparent if you have none.

    def render(self, screen):
        screen.blit(self.image, self.pos)
        # Assuming you have a textRenderer object to draw the quantity.
        textRenderer.render(screen, str(self.quantity), (self.pos[0]+30, self.pos[1]+30), 20, (255,255,255))

    def update(self):
        pass

    def handleInput(self, events):
        pass