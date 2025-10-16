from utils import *



class Patient:
    def __init__(self):
        # self.image = random.randint()
        self.image = pygame.transform.scale_by(pygame.image.load("images/patients/patient1.png"), .3)
        self.askingBubble = pygame.Surface([150,100])
        self.askingBubble.fill((255,255,255))
        self.pos = [2500,250]
        self.endPos = random.randint(100,1200)
        self.speed = random.randint(1,5)
        self.walking = True
        self.asking = False

    def render(self, screen):
        screen.blit(self.image, (self.pos[0], self.pos[1]))
        if self.asking:
            screen.blit(self.askingBubble, (self.pos[0]-85, self.pos[1]-60))

    def update(self):
        if self.walking:
            if self.pos[0] > self.endPos:
                self.pos[0] -= self.speed
            else:
                self.walking = False
                self.asking = True



class EasyPatient(Patient):
    def __init__(self):
        super().__init__()
        self.illness = random.choice(["die of beetus", "itchy pp", "sniffles"])

    def render(self, screen):
        super().render(screen)