import pygame
import random
from entities.base_entity import BaseEntity

class Meteor(BaseEntity):
    def __init__(self, word, speed):
        # Gunakan ukuran 50x50 agar pas dengan layar 405
        size = 50
        try:
            # Gunakan path yang benar (tanpa double assets/images)
            img = pygame.image.load("assets/images/bajigur.png").convert_alpha()
            img = pygame.transform.scale(img, (size, size))
        except:
            img = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(img, (139, 69, 19), (size//2, size//2), size//2 - 5)
        
        x_pos = random.randint(30, 325) 
        
        super().__init__(x_pos, -100, img)
        
        self.word = word
        self.speed = speed
        self.font = pygame.font.SysFont("Consolas", 22, bold=True)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen, is_target=False):
        super().draw(screen)
        color = (0, 255, 0) if is_target else (255, 255, 255)
        txt = self.font.render(self.word, True, color)
        
        # Posisi teks di atas meteor
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.y - 25))