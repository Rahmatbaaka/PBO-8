import pygame
from scenes.menu import MainMenu
from scenes.game_play import GamePlay

class MainController:
    def __init__(self):
        pygame.init()
        self.width, self.height = 405, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Typing Meteor Game")
        
        self.user_data = {
            "current_ship": "assets/images/Galaxy Bomber-baaka.png",
            "current_bg": "assets/images/planet asing.png"
        }
        
        self.state = "MENU"
        self.current_scene = MainMenu(self.screen, self.user_data, self.width, self.height)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                
                next_state = self.current_scene.handle_event(event)
                if next_state: self.change_scene(next_state)

            self.current_scene.update()
            self.current_scene.draw()
            pygame.display.flip()
            clock.tick(60)

    def change_scene(self, next_state):
        if next_state == "PLAYING":
            self.current_scene = GamePlay(self.screen, self.user_data, self.width, self.height)
        elif next_state == "MENU":
            self.current_scene = MainMenu(self.screen, self.user_data, self.width, self.height)
        elif next_state == "QUIT":
            pygame.quit()
            exit()

if __name__ == "__main__":
    game = MainController()
    game.run()