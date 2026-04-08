import pygame

class BaseEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        # Langsung simpan objek gambar, jangan di-load lagi di sini
        self.image = image 
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)