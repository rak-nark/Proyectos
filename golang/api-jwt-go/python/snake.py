import pygame
import sys
import random
from typing import Tuple, Set, Optional

# Inicializar Pygame
pygame.init()

class Config:
    # Configuración de pantalla
    WIDTH = 800
    HEIGHT = 600
    CELL_SIZE = 20
    FPS = 10
    
    # Configuración del juego
    INITIAL_SNAKE_LENGTH = 3
    WALL_COUNT = 10
    SPECIAL_FOOD_CHANCE = 2
    SPEED_INCREASE_RATE = 5
    
    # Colores
    COLORS = {
        'WHITE': (255, 255, 255),
        'BLACK': (0, 0, 0),
        'GREEN': (0, 128, 0),
        'RED': (255, 0, 0),
        'GRAY': (128, 128, 128),
        'GOLD': (255, 215, 0)
    }

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        sound_files = {
            'eat': 'eat.wav',
            'special': 'special.wav',
            'game_over': 'game_over.wav'
        }
        for name, file in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(file)
            except FileNotFoundError:
                print(f"Warning: Sound file {file} not found")
                
    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = self._load_high_score()
    
    def _load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except:
            return 0
            
    def save_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            try:
                with open('high_score.txt', 'w') as f:
                    f.write(str(self.high_score))
            except:
                print("Error saving high score")
    
    def add_points(self, points):
        self.current_score += points
        self.save_high_score()

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [(Config.WIDTH // 2, Config.HEIGHT // 2)]
        self.direction = (Config.CELL_SIZE, 0)
        self.growing = False
        self.last_direction = self.direction
    
    def change_direction(self, new_direction):
        opposite_direction = (-new_direction[0], -new_direction[1])
        if self.last_direction != opposite_direction:
            self.direction = new_direction
    
    def move(self):
        self.last_direction = self.direction
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        if self.growing:
            self.body = [new_head] + self.body
            self.growing = False
        else:
            self.body = [new_head] + self.body[:-1]
    
    def grow(self):
        self.growing = True
    
    def check_collision(self, walls: Set[Tuple[int, int]], edges: bool = True) -> bool:
        head = self.body[0]
        # Colisión con los bordes
        if edges and (
            head[0] < 0 or 
            head[0] >= Config.WIDTH or 
            head[1] < 0 or 
            head[1] >= Config.HEIGHT
        ):
            return True
        # Colisión con el cuerpo
        if head in self.body[1:]:
            return True
        # Colisión con paredes
        if head in walls:
            return True
        return False
    
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(
                surface, 
                Config.COLORS['GREEN'], 
                (*segment, Config.CELL_SIZE, Config.CELL_SIZE)
            )

class Food:
    def __init__(self, color=Config.COLORS['RED'], avoid_positions: Set[Tuple[int, int]] = None):
        self.color = color
        self.avoid_positions = avoid_positions or set()
        self.position = self.random_position()
    
    def random_position(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, (Config.WIDTH - Config.CELL_SIZE) // Config.CELL_SIZE) * Config.CELL_SIZE
            y = random.randint(0, (Config.HEIGHT - Config.CELL_SIZE) // Config.CELL_SIZE) * Config.CELL_SIZE
            pos = (x, y)
            if pos not in self.avoid_positions:
                return pos
    
    def draw(self, surface):
        pygame.draw.rect(
            surface, 
            self.color, 
            (*self.position, Config.CELL_SIZE, Config.CELL_SIZE)
        )

class Wall:
    def __init__(self, snake_positions: Set[Tuple[int, int]]):
        self.blocks = set()
        self._generate_walls(snake_positions)
    
    def _generate_walls(self, snake_positions: Set[Tuple[int, int]]):
        attempts = 0
        while len(self.blocks) < Config.WALL_COUNT and attempts < 100:
            x = random.randint(0, (Config.WIDTH - Config.CELL_SIZE) // Config.CELL_SIZE) * Config.CELL_SIZE
            y = random.randint(0, (Config.HEIGHT - Config.CELL_SIZE) // Config.CELL_SIZE) * Config.CELL_SIZE
            pos = (x, y)
            if pos not in snake_positions and pos not in self.blocks:
                self.blocks.add(pos)
            attempts += 1
    
    def draw(self, surface):
        for block in self.blocks:
            pygame.draw.rect(
                surface, 
                Config.COLORS['GRAY'], 
                (*block, Config.CELL_SIZE, Config.CELL_SIZE)
            )

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption("Snake - Juego Mejorado")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 35)
        self.large_font = pygame.font.SysFont(None, 55)
        
        self.sound_manager = SoundManager()
        self.score_manager = ScoreManager()
        self.state = GameState.MENU
        self.difficulty = None
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.special_food = None
        self.wall = Wall(set(self.snake.body))
        self.score_manager.current_score = 0
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    
    def handle_keydown(self, key):
        if self.state == GameState.PLAYING:
            self.handle_playing_keys(key)
        elif self.state == GameState.MENU:
            self.handle_menu_keys(key)
        elif self.state == GameState.GAME_OVER:
            self.handle_game_over_keys(key)
    
    def handle_playing_keys(self, key):
        if key == pygame.K_UP and self.snake.direction != (0, Config.CELL_SIZE):
            self.snake.change_direction((0, -Config.CELL_SIZE))
        elif key == pygame.K_DOWN and self.snake.direction != (0, -Config.CELL_SIZE):
            self.snake.change_direction((0, Config.CELL_SIZE))
        elif key == pygame.K_LEFT and self.snake.direction != (Config.CELL_SIZE, 0):
            self.snake.change_direction((-Config.CELL_SIZE, 0))
        elif key == pygame.K_RIGHT and self.snake.direction != (-Config.CELL_SIZE, 0):
            self.snake.change_direction((Config.CELL_SIZE, 0))
        elif key == pygame.K_p:
            self.toggle_pause()
    
    def handle_menu_keys(self, key):
        if key == pygame.K_1:
            self.difficulty = "easy"
            self.state = GameState.PLAYING
        elif key == pygame.K_2:
            self.difficulty = "hard"
            self.state = GameState.PLAYING
    
    def handle_game_over_keys(self, key):
        if key == pygame.K_r:
            self.reset_game()
            self.state = GameState.MENU
        elif key == pygame.K_q:
            self.quit_game()
    
    def toggle_pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
            
        self.snake.move()
        
        # Comprobar colisiones
        if self.difficulty == "hard" and self.snake.check_collision(self.wall.blocks):
            self.sound_manager.play('game_over')
            self.state = GameState.GAME_OVER
            return
        
        # Comprobar comida
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.sound_manager.play('eat')
            self.score_manager.add_points(1)
            self.food = Food(avoid_positions=self.wall.blocks)
        
        # Comprobar comida especial
        if self.special_food and self.snake.body[0] == self.special_food.position:
            self.snake.grow()
            self.sound_manager.play('special')
            self.score_manager.add_points(5)
            self.special_food = None
        
        # Generar comida especial
        if random.randint(1, 100) <= Config.SPECIAL_FOOD_CHANCE and not self.special_food:
            self.special_food = Food(color=Config.COLORS['GOLD'], avoid_positions=self.wall.blocks)
    
    def draw(self):
        self.screen.fill(Config.COLORS['BLACK'])
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self.draw_game()
            if self.state == GameState.PAUSED:
                self.draw_pause_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        easy_text = self.large_font.render("Dificultad: Fácil (Sin colisiones)", True, Config.COLORS['WHITE'])
        hard_text = self.large_font.render("Dificultad: Maestro Estelar (Con colisiones)", True, Config.COLORS['WHITE'])
        select_text = self.font.render("Presiona 1 para Fácil o 2 para Maestro Estelar", True, Config.COLORS['WHITE'])
        
        self.screen.blit(easy_text, (Config.WIDTH // 2 - easy_text.get_width() // 2, Config.HEIGHT // 3))
        self.screen.blit(hard_text, (Config.WIDTH // 2 - hard_text.get_width() // 2, Config.HEIGHT // 2))
        self.screen.blit(select_text, (Config.WIDTH // 2 - select_text.get_width() // 2, Config.HEIGHT // 1.5))
    
    def draw_game(self):
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        if self.special_food:
            self.special_food.draw(self.screen)
        self.wall.draw(self.screen)
        self.draw_score()
    
    def draw_pause_screen(self):
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        overlay.fill(Config.COLORS['BLACK'])
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.large_font.render("JUEGO PAUSADO", True, Config.COLORS['WHITE'])
        continue_text = self.font.render("Presiona P para continuar", True, Config.COLORS['WHITE'])
        
        self.screen.blit(pause_text, (Config.WIDTH // 2 - pause_text.get_width() // 2, Config.HEIGHT // 3))
        self.screen.blit(continue_text, (Config.WIDTH // 2 - continue_text.get_width() // 2, Config.HEIGHT // 2))
    
    def draw_game_over(self):
        game_over_text = self.large_font.render("¡Game Over!", True, Config.COLORS['RED'])
        score_text = self.font.render(f"Tu puntuación: {self.score_manager.current_score}", True, Config.COLORS['WHITE'])
        high_score_text = self.font.render(f"Mejor puntuación: {self.score_manager.high_score}", True, Config.COLORS['WHITE'])
        retry_text = self.font.render("Presiona R para reiniciar o Q para salir", True, Config.COLORS['WHITE'])
        
        self.screen.blit(game_over_text, (Config.WIDTH // 2 - game_over_text.get_width() // 2, Config.HEIGHT // 5))
        self.screen.blit(score_text, (Config.WIDTH // 2 - score_text.get_width() // 2, Config.HEIGHT // 3))
        self.screen.blit(high_score_text, (Config.WIDTH // 2 - high_score_text.get_width() // 2, Config.HEIGHT // 2.5))
        self.screen.blit(retry_text, (Config.WIDTH // 2 - retry_text.get_width() // 2, Config.HEIGHT // 2))
    

    def draw_score(self):
        score_text = self.font.render(f"Puntuación: {self.score_manager.current_score}", True, Config.COLORS['WHITE'])
        high_score_text = self.font.render(f"Mejor: {self.score_manager.high_score}", True, Config.COLORS['WHITE'])
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
    
    def quit_game(self):
        self.score_manager.save_high_score()
        pygame.quit()
        sys.exit()
    
    def run(self):
        while True:
            self.clock.tick(Config.FPS + self.score_manager.current_score // Config.SPEED_INCREASE_RATE)
            self.handle_input()
            self.update()
            self.draw()

def main():
    game = Game()
    try:
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()







    