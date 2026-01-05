from uiClasses import *


class Patient:
    def __init__(self, walkingAnimation, idleAnimation, talkingAnimation, currentState, pos, endPos, speed, id, illness):
        self.illness = illness
        self.id = id
        self.walkingAnimation = Animation(walkingAnimation["path"], walkingAnimation["images"], walkingAnimation["duration"], walkingAnimation["scale"], walkingAnimation["isFlipped"])
        self.idleAnimation = Animation(idleAnimation["path"], idleAnimation["images"], idleAnimation["duration"], idleAnimation["scale"], idleAnimation["isFlipped"])
        self.talkingAnimation = Animation(talkingAnimation["path"], talkingAnimation["images"], talkingAnimation["duration"], talkingAnimation["scale"], talkingAnimation["isFlipped"])
        self.states = {
            "walking": self.walkingAnimation,
            "talking": self.talkingAnimation,
            "idling": self.idleAnimation
        }
        self.currentState = currentState
        self.askingBubble = pygame.transform.smoothscale_by(pygame.image.load("images/ui/bubble.png"), .2)
        self.bubbleText = random.choice(["Dear god help me", "It hurts.", "I need to poop!", "Owwie ;n;", "I want my mommy.", "The plague!!!", "Meow"])
        self.pos = pos
        self.endPos = endPos
        self.image = self.states["talking"].images[0]
        self.rect = pygame.Rect(pos[0],pos[1], self.image.get_width(),self.image.get_height())
        self.rect.y = 700 - self.rect.h
        self.pos[1] = self.rect.y
        self.speed = speed

        self.waiting = True
        self.inARoom = False

    def render(self, screen):
        self.states[self.currentState].render(screen, self.pos)
        if self.currentState == "talking":
            screen.blit(self.askingBubble, (self.pos[0]+75, self.pos[1]-160))
            textRenderer.render(self.askingBubble, self.bubbleText, (130,100), 20, (0,0,0), align="center")
        
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)


    def update(self):
        self.states[self.currentState].update()
        self.rect.x = self.pos[0] + 30
        self.rect.y = self.pos[1]
        if self.currentState == "walking":
            if self.pos[0] > self.endPos:
                self.pos[0] -= self.speed
            else:
                self.currentState = "talking"
                
        if self.inARoom and self.currentState == "talking":
            self.currentState == "idling"


    def checkClick(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def toDict(self):
        pass


class PatientInVetRoom:
    def __init__(self, animalName, illness):
        self.animalName = animalName
        self.animalData = patientInfo[animalName]
        self.illness = illness

        self.walkingAnimation = Animation(
            self.animalData["walkingAnimation"]["path"], 
            self.animalData["walkingAnimation"]["images"], 
            self.animalData["walkingAnimation"]["duration"],
            self.animalData["walkingAnimation"]["scale"],
            self.animalData["walkingAnimation"]["isFlipped"]
        )

        self.idleAnimations = []
        for animation in self.animalData["idleAnimations"]:
            self.idleAnimations.append(Animation(
                animation["path"],
                animation["images"],
                animation["duration"],
                animation["scale"],
                animation["isFlipped"]
            ))