import pygame

class Boatmaster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/images/ship_captain.png')
        self.image = pygame.transform.scale(self.image, (200, 175))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.channel = None
        self.talking = False
        self.fading = False
        self.has_spoken_1 = False
        self.has_spoken_2 = False
        self.fade_alpha = 255
        self.original_image = self.image.copy()

    def update(self):
        if self.talking and self.channel and not self.channel.get_busy():
            self.stop_talking_1()
            self.stop_talking_2()
        if self.fading:
            self.fade_alpha -= 20
            if self.fade_alpha <= 0:
                self.kill()
            else:
                self.image.set_alpha(self.fade_alpha)

    def speak_no_kibble(self, screen):
        # draw the textbox
        text_box = pygame.Rect(100, 300, 700, 185)
        pygame.draw.rect(screen, (0, 0, 0), text_box)
        pygame.draw.rect(screen, (255, 255, 255), text_box, 2)

        # draw the text
        font = pygame.font.Font('freesansbold.ttf', 20)

        message = (
            "Hello young Frog, I am the local boatmaster. "
            "I have several hungry cats at home, and I was wondering if you could procure 3 bags of kibble for me."
            "As you can probably imagine,being a boatmaster with no ocean, has posed some challenges."
            "That's why I have resorted to driving a covered-wagon."
            "Anyways, procure the kibble and i'll take you to the princess."
        )

        import textwrap
        lines = textwrap.wrap(message, width=65)

        y = text_box.y + 20
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (text_box.x + 20, y))
            y += font.get_height() + 5

            pygame.display.flip()



    def speak_kibble(self, screen):
        # draw the textbox
        text_box = pygame.Rect(100, 300, 700, 185)
        pygame.draw.rect(screen, (0, 0, 0), text_box)
        pygame.draw.rect(screen, (255, 255, 255), text_box, 2)

        # draw the text
        font = pygame.font.Font('freesansbold.ttf', 20)

        message = (
            "Great, hop aboard."
        )

        import textwrap
        lines = textwrap.wrap(message, width=25)

        y = text_box.y + 20
        for line in lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (text_box.x + 20, y))
            y += font.get_height() + 5

            pygame.display.flip()
            pygame.time.delay(2000)

    def speech_no_kibble(self, sound):
        print("Speech no kibble triggered")
        self.dialogue_type = "no kibble"
        self.channel = sound.play()
        self.talking = True

    def speech_kibble(self, sound):
        print("Speech with kibble triggered")
        self.dialogue_type = "kibble"
        self.channel = sound.play()
        self.talking = True

    def start_talking(self, kibble_collected, screen):
        if not self.talking:
            if kibble_collected:
                sound = pygame.mixer.Sound("assets/sounds/boatmaster_kibble.wav")
                self.speech_kibble(sound)
                self.speak_kibble(screen)

            else:
                sound = pygame.mixer.Sound("assets/sounds/boatmaster_no_kibble.wav")
                self.speech_no_kibble(sound)
                self.speak_no_kibble(screen)

    def stop_talking_1(self):
        if self.channel and self.channel.get_busy():
            self.channel.stop()
        self.talking = False
        self.fading = True
        self.finished_first_speech = True
        self.has_spoken_1 = True

    def stop_talking_2(self):
        if self.channel and self.channel.get_busy():
            self.channel.stop()
        self.talking = False
        self.fading = True
        self.has_spoken_2 = True
        self.kill()
