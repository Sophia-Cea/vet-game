from uiClasses import *



class Patient:
    def __init__(self):
        self.walkingAnimation = Animation("images/patients/paige/", [
            "paigeWalking1.png",
            "paigeWalking2.png",
            "paigeWalking3.png",
            "paigeWalking4.png"
        ], 1, .4, True)
        self.idleAnimation = Animation("images/patients/paige/", [
            "paigeIdle1.png"
        ], 3, .4)
        self.states = {
            "walking": self.walkingAnimation,
            "talking": None,
            "idling": self.idleAnimation
        }
        self.currentState = "walking"
        self.askingBubble = pygame.Surface([150,100])
        self.askingBubble.fill((255,255,255))
        self.pos = [1500,250]
        self.endPos = random.randint(100,1200)
        self.speed = random.randint(1,5)
        self.asking = False

    def render(self, screen):
        self.states[self.currentState].render(screen, self.pos)
        if self.asking:
            screen.blit(self.askingBubble, (self.pos[0]-85, self.pos[1]-60))

    def update(self):
        self.states[self.currentState].update()
        if self.currentState == "walking":
            if self.pos[0] > self.endPos:
                self.pos[0] -= self.speed
            else:
                self.currentState = "idling"
                self.asking = True



class EasyPatient(Patient):
    def __init__(self):
        super().__init__()
        self.illness = random.choice(["die of beetus", "itchy pp", "sniffles"])

    def render(self, screen):
        super().render(screen)