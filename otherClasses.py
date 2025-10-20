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
        self.categories = {}
        j = 0
        for category_name, ingredients_dict in potionInfo["potion ingredients"].items():
            if category_name == "path":
                continue
            self.categories[category_name] = []
            i = 0
            for ingredient_name, ingredient_data in ingredients_dict.items():
                ingredient = PotionIngredient(
                    name=ingredient_name,
                    category=category_name,
                    pos=[160+(i%6)*70, 170+i//6],
                    quantity=ingredient_data["quantity"],
                    scale=ingredient_data["scale"],
                    leftSide=(j%2==1)
                )
                self.categories[category_name].append(ingredient)
                i += 1
            j += 1

        self.currentWindow = 0
        category_keys = list(self.categories.keys())
        self.activeCategories = [category_keys[self.currentWindow], category_keys[self.currentWindow + 1]]


    def render(self, screen):
        screen.blit(self.ingredientMenu, (10,10))
        screen.blit(self.ingredientMenu, (10,10))

        for category in self.activeCategories:
            for item in self.categories[category]:
                item.render(screen)

    def update(self):
        pass

    def handleInput(self, events):
        pass


class PotionIngredient:
    def __init__(self, name, category, pos, quantity, scale, leftSide=True):
        self.image = pygame.transform.scale_by(pygame.image.load(potionInfo["potion ingredients"]["path"] + potionInfo["potion ingredients"][category][name]["path"]).convert_alpha(), scale)
        self.pos = pos
        if leftSide:
            self.pos[0] += 730
        self.quantity = quantity
        if self.quantity == 0:
            self.image.set_alpha(60)

    def render(self, screen):
        screen.blit(self.image, self.pos)
        textRenderer.render(screen, str(self.quantity), (self.pos[0]+30, self.pos[1]+30), 20, (255,255,255))

    def update(self):
        pass

    def handleInput(self, events):
        pass