from uiClasses import *



class Patient:
    def __init__(self, walkingAnimation, idleAnimation, talkingAnimation, currentState, pos, endPos, speed, id):
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
        self.pos = pos
        self.endPos = endPos
        self.speed = speed
        self.index = None 
        for i, patient in enumerate(GameData.activePatients):
            # print(patient)
            # print(patient["id"])
            # print(self.id)
            if patient["id"] == self.id:
                self.index = i

    def render(self, screen):
        self.states[self.currentState].render(screen, self.pos)
        if self.currentState == "talking":
            screen.blit(self.askingBubble, (self.pos[0]+75, self.pos[1]-160))

    def update(self):
        self.states[self.currentState].update()
        if self.currentState == "walking":
            if self.pos[0] > self.endPos:
                self.pos[0] -= self.speed
            else:
                self.currentState = "talking"
        GameData.activePatients[self.index]["pos"] = self.pos
        GameData.activePatients[self.index]["state"] = self.currentState



class EasyPatient(Patient):
    def __init__(self):
        super().__init__()
        self.illness = random.choice(["die of beetus", "itchy pp", "sniffles"])

    def render(self, screen):
        super().render(screen)