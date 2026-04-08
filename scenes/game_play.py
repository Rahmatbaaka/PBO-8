import pygame
import random
import json
from entities.meteor import Meteor
from entities.ship import Ship

class GamePlay:
    def __init__(self, screen, user_data, width, height):
        self.screen, self.width, self.height = screen, width, height
        self.user_data = user_data
        
        bg_path = user_data['current_bg']
        full_bg_path = bg_path if bg_path.startswith("assets/") else f"assets/images/{bg_path}"
        try:
            self.bg = pygame.image.load(full_bg_path).convert()
            self.bg = pygame.transform.scale(self.bg, (width, height))
        except:
            self.bg = pygame.Surface((width, height))
            self.bg.fill((5, 5, 20))
            
        try:
            with open("data/level_words.json", "r") as f:
                self.word_pool = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            self.word_pool = {"level_1": ["PYTHON", "OBJECT", "CLASS"]}
            
        self.level, self.hp, self.score = 1, 5, 0
        self.meteors, self.target_meteor = [], None
        self.spawn_timer = 0
        self.font_ui = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_pop = pygame.font.SysFont("Consolas", 30, bold=True)
        
        self.game_over = False 
        self.player_ship = Ship(width//2 - 30, height - 100, user_data["current_ship"])

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y: return "PLAYING" 
                if event.key == pygame.K_n: return "MENU"    
            return None

        if event.type == pygame.KEYDOWN:
            char = event.unicode.upper()
            if not self.target_meteor:
                for m in self.meteors:
                    if m.word.startswith(char):
                        self.target_meteor = m
                        self.strike()
                        break
            elif self.target_meteor.word.startswith(char):
                self.strike()
        return None

    def strike(self):
        self.target_meteor.word = self.target_meteor.word[1:]
        self.score += 5
        if not self.target_meteor.word:
            self.meteors.remove(self.target_meteor)
            self.target_meteor = None
            if self.score % 100 == 0 and self.level < 8:
                self.level += 1

    def update(self):
        if self.game_over: return None
        if self.hp <= 0:
            self.hp = 0
            self.game_over = True
            return None

        speed = 0.7 + (self.level * 0.15)
        
        self.spawn_timer += 1
        if self.spawn_timer > 100:
            level_key = f"level_{self.level}"
            words_in_level = self.word_pool.get(level_key, self.word_pool["level_1"])
            word = random.choice(words_in_level).upper()
            
            self.meteors.append(Meteor(word, speed))
            self.spawn_timer = 0

        for m in self.meteors[:]:
            m.update()
            if m.rect.y > self.height - 60:
                self.hp -= 1
                self.meteors.remove(m)
                if self.target_meteor == m: self.target_meteor = None
        
        target_x = self.target_meteor.rect.x if self.target_meteor else self.width//2 - 30
        self.player_ship.update(target_x)
        return None

    def draw(self):
        self.screen.blit(self.bg, (0,0))
        for m in self.meteors:
            m.draw(self.screen, m == self.target_meteor)
        self.player_ship.draw(self.screen)
        
        pygame.draw.rect(self.screen, (0,0,0, 150), (0, 0, self.width, 40))
        ui_text = f"HP: {self.hp} | SCORE: {self.score} | LVL: {self.level}"
        ui_surf = self.font_ui.render(ui_text, True, (255, 255, 255))
        self.screen.blit(ui_surf, (15, 10))

        if self.game_over:
            self.draw_popup()

    def draw_popup(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))
        
        pw, ph = 320, 200
        px, py = self.width//2 - pw//2, self.height//2 - ph//2
        pygame.draw.rect(self.screen, (30, 30, 50), (px, py, pw, ph), border_radius=15)
        pygame.draw.rect(self.screen, (0, 255, 255), (px, py, pw, ph), 3, border_radius=15)

        t1 = self.font_pop.render("GAME OVER", True, (255, 50, 50))
        t2 = self.font_ui.render(f"Final Score: {self.score}", True, (255, 255, 255))
        t3 = self.font_ui.render("Lanjut Main? (Y/N)", True, (0, 255, 0))
        
        self.screen.blit(t1, (self.width//2 - t1.get_width()//2, py + 30))
        self.screen.blit(t2, (self.width//2 - t2.get_width()//2, py + 80))
        self.screen.blit(t3, (self.width//2 - t3.get_width()//2, py + 130))