import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()
WIDTH, HEIGHT = 1080, 800
CELL_SIZE = 50
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)      # Fácil
ORANGE = (255, 165, 0) # Médio
GREEN = (0, 255, 0)    # Difícil
GRAY = (200, 200, 200)
DARK_BROWN = (101, 67, 33)
ROAD_COLOR = (0, 0, 0)
BLUE = (0, 0, 255)     # Torre tipo 1
YELLOW = (255, 255, 0) # Torre tipo 2
PURPLE = (128, 0, 128) # Torre tipo 3

# Imagens
TOWER_IMAGE_1 = pygame.image.load("tower-1.png")
TOWER_IMAGE_1 = pygame.transform.scale(TOWER_IMAGE_1, (30, 30))

# Pontos e custos
player_points = 0
player_money = 10000
tower_costs = [50, 100, 200]
reward_enemy = [10, 25, 100]
points_enemy = [20, 100, 200]
lives = 2000
available_towers = float('inf')
current_level = 0

# Níveis de dificuldade
levels = [
    (20, 5, 1),
    (60, 15, 3),
    (100, 30, 6),
    (160, 45, 12),
    (200, 60, 20),
]

# Caminho para os inimigos
path = [
    (1 * CELL_SIZE + 25, 0 * CELL_SIZE + 25), 
    (1 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
    (10 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
    (10 * CELL_SIZE + 25, 1 * CELL_SIZE + 25),
    (16 * CELL_SIZE + 25, 1 * CELL_SIZE + 25), 
    (16 * CELL_SIZE + 25, 7 * CELL_SIZE + 25),
    (7 * CELL_SIZE + 25, 7 * CELL_SIZE + 25), 
    (7 * CELL_SIZE + 25, 10 * CELL_SIZE + 25),
    (1 * CELL_SIZE + 25, 10 * CELL_SIZE + 25), 
    (1 * CELL_SIZE + 25, 13 * CELL_SIZE + 25),
    (17 * CELL_SIZE + 25, 13 * CELL_SIZE + 25), 
    (17 * CELL_SIZE + 25, 17 * CELL_SIZE + 25),
    (17 * CELL_SIZE + 25, HEIGHT + 0)
]

# Classe Inimigo
class Enemy:
    def __init__(self, path, difficulty):
        self.path = path
        self.x, self.y = path[0]
        self.speed = 1
        self.health = 30 * difficulty
        self.current_point = 0
        self.color = self.get_color(difficulty)
        self.difficulty = difficulty

    def get_color(self, difficulty):
        return [RED, ORANGE, GREEN][difficulty - 1]

    def move(self):
        if self.current_point < len(self.path) - 1:
            target_x, target_y = self.path[self.current_point + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < self.speed:
                self.x, self.y = target_x, target_y
                self.current_point += 1
            else:
                self.x += dx / distance * self.speed
                self.y += dy / distance * self.speed

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (int(self.x), int(self.y)), 10)
        # Barra de vida
        health_bar_length = 20
        health_ratio = self.health / (30 * 3)
        pygame.draw.rect(SCREEN, WHITE, (self.x - health_bar_length / 2, self.y - 15, health_bar_length, 5))
        pygame.draw.rect(SCREEN, (0, 255, 0), (self.x - health_bar_length / 2, self.y - 15, health_bar_length * health_ratio, 5))

# Classe Torre
class Tower:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = {50: [0.1, 0.05, 0.01], 100: [0.25, 0.15, 0.05], 200: [0.5, 0.35, 0.15]}[cost]
        self.cost = cost
        self.cooldown = 60
        self.timer = 0

    def attack(self, enemies):
        if self.timer == 0:
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if distance <= self.range:
                    enemy.health -= self.damage[enemy.difficulty - 1] * 30
                    self.timer = self.cooldown
                    return True
        return False

    def draw(self):
        tower_rect = TOWER_IMAGE_1.get_rect(center=(self.x, self.y))
        SCREEN.blit(TOWER_IMAGE_1, tower_rect)  # Desenha a imagem da torre na posição correta
        
        
        # Desenha o alcance da torre
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.range, 1)

    def update(self):
        if self.timer > 0:
            self.timer -= 1

# Funções auxiliares
def draw_menu():
    pygame.draw.rect(SCREEN, GRAY, (WIDTH - 150, 0, 150, HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Moedas: {player_money}", True, BLACK)
    SCREEN.blit(text, (WIDTH - 140, 10))
    lives_text = font.render(f"Vidas: {lives}", True, BLACK)
    SCREEN.blit(lives_text, (WIDTH - 140, 50))

    for i, cost in enumerate(tower_costs):
        color = BLUE if cost == 50 else YELLOW if cost == 100 else PURPLE
        pygame.draw.circle(SCREEN, color, (WIDTH - 75, 150 + i * 50), 15)
        SCREEN.blit(font.render(str(cost), True, BLACK), (WIDTH - 100, 140 + i * 50))

def generate_enemies():
    f, m, d = levels[current_level]
    difficulty_counts = [(1, f), (2, m), (3, d)]
    for difficulty, count in difficulty_counts:
        for _ in range(count):
            enemy_queue.append(Enemy(path, difficulty))

# Inicializar lista de inimigos, fila de inimigos e torres
enemies = []
enemy_queue = []
towers = []
enemy_spawn_timer = 0
spawn_interval = 30  # intervalo para cada inimigo aparecer
selected_tower_cost = None

# Loop principal do jogo
running = True
generate_enemies()  # Gerar inimigos ao iniciar o jogo

while running:
    SCREEN.fill(DARK_BROWN)
    for i in range(len(path) - 1):
        pygame.draw.line(SCREEN, ROAD_COLOR, path[i], path[i + 1], 10)

    # Desenhar a grade e verificar eventos
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (WIDTH, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

            if mouse_x > WIDTH - 150:
                for i, cost in enumerate(tower_costs):
                    if 150 + i * 50 < mouse_y < 150 + (i + 1) * 50 and player_money >= cost:
                        selected_tower_cost = cost
                        player_money -= cost
                        towers.append(Tower(grid_x * CELL_SIZE + 25, grid_y * CELL_SIZE + 25, selected_tower_cost))

            elif selected_tower_cost:
                towers.append(Tower(grid_x * CELL_SIZE + 25, grid_y * CELL_SIZE + 25, selected_tower_cost))
                selected_tower_cost = None

    # Atualizar e desenhar torres
    for tower in towers:
        tower.update()
        tower.attack(enemies)
        tower.draw()

    # Atualizar e desenhar inimigos
    for enemy in enemies:
        enemy.move()
        enemy.draw()
        if enemy.health <= 0:
            player_points += reward_enemy[enemy.difficulty - 1]
            enemies.remove(enemy)
        if enemy.current_point >= len(path) - 1:  # Inimigo chegou ao fim
            lives -= 1
            enemies.remove(enemy)

    # Atualiza o spawn de inimigos
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= spawn_interval:
        if enemy_queue:
            enemies.append(enemy_queue.pop(0))
        enemy_spawn_timer = 0

    # Desenhar menu
    draw_menu()

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
sys.exit()
