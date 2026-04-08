import pygame

class MainMenu:
    def __init__(self, screen, user_data, width, height):
        self.screen, self.width, self.height = screen, width, height
        self.font_title = pygame.font.SysFont("Consolas", 45, bold=True)
        self.font_btn = pygame.font.SysFont("Consolas", 25)

        bw, bh = 200, 50
        self.btn_start = pygame.Rect(width//2 - bw//2, 300, bw, bh)
        self.btn_quit = pygame.Rect(width//2 - bw//2, 380, bw, bh)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_start.collidepoint(event.pos): return "PLAYING"
            if self.btn_quit.collidepoint(event.pos): return "QUIT"
        return None

    def update(self): 
        pass 

    def draw(self):
        self.screen.fill((10, 10, 30))
        title = self.font_title.render("BAAKA TYPING", True, (0, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 150))
        
        for txt, rect in [("START", self.btn_start), ("QUIT", self.btn_quit)]:
            pygame.draw.rect(self.screen, (50, 50, 80), rect, border_radius=10)
            t_surf = self.font_btn.render(txt, True, (255, 255, 255))
            self.screen.blit(t_surf, t_surf.get_rect(center=rect.center))