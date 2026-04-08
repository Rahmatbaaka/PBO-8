import pygame
from entities.base_entity import BaseEntity

class Ship(BaseEntity):
    def __init__(self, x, y, img_path):
        # img_path biasanya berisi "pesawat/ship_red.png"
        full_path = f"{img_path}"
        
        try:
            img_surface = pygame.image.load(full_path).convert_alpha()
            img_surface = pygame.transform.scale(img_surface, (80, 80))
        except:
            print(f"Gagal memuat: {full_path}. Menggunakan placeholder.")
            img_surface = pygame.Surface((80, 80))
            img_surface.fill((0, 255, 0)) # Hijau jika gagal
            
        # Kirim objek gambar yang sudah jadi ke BaseEntity
        super().__init__(x, y, img_surface)

    def update(self, target_x):
        # Pergerakan halus mengikuti meteor
        self.rect.x += (target_x - self.rect.x) * 0.1