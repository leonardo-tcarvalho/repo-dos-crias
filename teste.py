import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()
CELL_SIZE = 50
WIDTH, HEIGHT = 18 * CELL_SIZE + 200, 800  # Ajusta a largura do mapa para 18 células + largura do menu
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
CYAN = (0, 255, 255)   # Torre tipo 4
MAGENTA = (255, 0, 255) # Torre tipo 5

# Imagens
TOWER_IMAGE_1 = pygame.image.load("assets/towers/tower-1.png")
TOWER_IMAGE_1 = pygame.transform.scale(TOWER_IMAGE_1, (30, 30))
TOWER_IMAGE_2 = pygame.image.load("assets/towers/tower-2.png")
TOWER_IMAGE_2 = pygame.transform.scale(TOWER_IMAGE_2, (30, 30))
TOWER_IMAGE_3 = pygame.image.load("assets/towers/tower-3.png")
TOWER_IMAGE_3 = pygame.transform.scale(TOWER_IMAGE_3, (30, 30))

ENEMY_IMAGE_1 = pygame.image.load("assets/enemys/enemy-1.png")
ENEMY_IMAGE_1 = pygame.transform.scale(ENEMY_IMAGE_1, (30, 30))
ENEMY_IMAGE_2 = pygame.image.load("assets/enemys/enemy-2.png")
ENEMY_IMAGE_2 = pygame.transform.scale(ENEMY_IMAGE_2, (40, 40))
ENEMY_IMAGE_3 = pygame.image.load("assets/enemys/enemy-3.png")
ENEMY_IMAGE_3 = pygame.transform.scale(ENEMY_IMAGE_3, (50, 50))

BULLET_IMAGE_1 = pygame.image.load("assets/bullets/bullet-1.png")
BULLET_IMAGE_1 = pygame.transform.scale(BULLET_IMAGE_1, (10, 10))
BULLET_IMAGE_2 = pygame.image.load("assets/bullets/bullet-2.png")
BULLET_IMAGE_2 = pygame.transform.scale(BULLET_IMAGE_2, (10, 10))
BULLET_IMAGE_3 = pygame.image.load("assets/bullets/bullet-3.png")
BULLET_IMAGE_3 = pygame.transform.scale(BULLET_IMAGE_3, (10, 10))

EFFECT_IMAGE_1 = pygame.image.load("assets/effect_bullet/effect-1.png")
EFFECT_IMAGE_1 = pygame.transform.scale(EFFECT_IMAGE_1, (40, 40))
EFFECT_IMAGE_2 = pygame.image.load("assets/effect_bullet/effect-2.png")
EFFECT_IMAGE_2 = pygame.transform.scale(EFFECT_IMAGE_2, (40, 40))
EFFECT_IMAGE_3 = pygame.image.load("assets/effect_bullet/effect-3.png")
EFFECT_IMAGE_3 = pygame.transform.scale(EFFECT_IMAGE_3, (40, 40))

EFFECT_IMAGES = [EFFECT_IMAGE_1, EFFECT_IMAGE_2, EFFECT_IMAGE_3]

# Imagens de decoração
TRUNK_IMAGE = pygame.image.load("assets/decorations/trunk.png")
TRUNK_IMAGE = pygame.transform.scale(TRUNK_IMAGE, (2 * CELL_SIZE, 2 * CELL_SIZE))
TREE_IMAGE = pygame.image.load("assets/decorations/tree.png")
TREE_IMAGE = pygame.transform.scale(TREE_IMAGE, (2 * CELL_SIZE, 2 * CELL_SIZE))
ROCK_IMAGE = pygame.image.load("assets/decorations/rock.png")
ROCK_IMAGE = pygame.transform.scale(ROCK_IMAGE, (2 * CELL_SIZE, 2 * CELL_SIZE))

# Posições das decorações para cada fase
decorations = {
    1: [
        (0 * CELL_SIZE - 1, 1 * CELL_SIZE - 1), 
        (5 * CELL_SIZE - 1, 6 * CELL_SIZE - 1), 
        (2 * CELL_SIZE - 1, 10 * CELL_SIZE - 1),
        (10 * CELL_SIZE - 1, 10 * CELL_SIZE - 1),
        (14 * CELL_SIZE - 1, 6 * CELL_SIZE - 1), 
        (7 * CELL_SIZE - 1, 2 * CELL_SIZE - 1),
        ],
    2: [
        (5 * CELL_SIZE - 1, 5 * CELL_SIZE - 1),
        (2 * CELL_SIZE - 1, 1 * CELL_SIZE - 1),
        (3 * CELL_SIZE - 1, 12 * CELL_SIZE - 1),
        (14 * CELL_SIZE - 1, 2 * CELL_SIZE - 1),
        (13 * CELL_SIZE - 1, 11 * CELL_SIZE - 1),
        (17 * CELL_SIZE - 1, 14 * CELL_SIZE - 1)
        ],
    3: [
        (14 * CELL_SIZE - 1, 1 * CELL_SIZE - 1),
        (6 * CELL_SIZE - 1, 0 * CELL_SIZE - 1),
        (2 * CELL_SIZE - 1, 9 * CELL_SIZE - 1),
        (0 * CELL_SIZE - 1, 3 * CELL_SIZE - 1),
        (9 * CELL_SIZE - 1, 8 * CELL_SIZE - 1),
        (10 * CELL_SIZE - 1, 14 * CELL_SIZE - 1)
        ],
    4: [
        (1 * CELL_SIZE - 1, 8 * CELL_SIZE - 1),
        (6 * CELL_SIZE - 1, 1 * CELL_SIZE - 1),
        (14 * CELL_SIZE - 1, 6 * CELL_SIZE - 1),
        (8 * CELL_SIZE - 1, 4 * CELL_SIZE - 1),
        (14 * CELL_SIZE - 1, 11 * CELL_SIZE - 1),
        (10 * CELL_SIZE - 1, 9 * CELL_SIZE - 1),
        (10 * CELL_SIZE - 1, 14 * CELL_SIZE - 1),
        (7 * CELL_SIZE - 1, 11 * CELL_SIZE - 1)
        ],
    5: [
        (2 * CELL_SIZE - 1, 7 * CELL_SIZE - 1),
        (3 * CELL_SIZE - 1, 1 * CELL_SIZE - 1),
        (7 * CELL_SIZE - 1, 5 * CELL_SIZE - 1),
        (14 * CELL_SIZE - 1, 9 * CELL_SIZE - 1),
        (13 * CELL_SIZE - 1, 4 * CELL_SIZE - 1),
        (2 * CELL_SIZE - 1, 11 * CELL_SIZE - 1),
        (10 * CELL_SIZE - 1, 14 * CELL_SIZE - 1),
        (9 * CELL_SIZE - 1, 10 * CELL_SIZE - 1)
        ],
}




def draw_decorations(level):
    decoration_positions = decorations.get(level, [])
    for i, (x, y) in enumerate(decoration_positions):
        decoration_image = [TRUNK_IMAGE, TREE_IMAGE, ROCK_IMAGE][i % 3]
        SCREEN.blit(decoration_image, (x, y))

# Pontos e custos
player_points = 0
player_money = 300
reward_enemy = [75, 150, 300]  # Update rewards for killing enemies
tower_costs = [50, 100, 200]
points_enemy = [50, 100, 200]
available_towers = float('inf')
current_level = 1  # Inicializa o nível atual como 1

# Níveis de dificuldade
qtdEnemysPerlevel = {
    1: (30, 5, 2),
    2: (60, 15, 6),
    3: (100, 30, 9),
    4: (160, 45, 12),
    5: (200, 60, 20),
}

# Caminho para os inimigos
pathLevels = {
    1: [
        (-1 * CELL_SIZE + 25, 4 * CELL_SIZE + 25), 
        (12 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
        (12 * CELL_SIZE + 25, 9 * CELL_SIZE + 25), 
        (14 * CELL_SIZE + 25, 9 * CELL_SIZE + 25),
        (14 * CELL_SIZE + 25, 15 * CELL_SIZE + 25), 
    ],
    2: [
        (-1 * CELL_SIZE + 25, 4 * CELL_SIZE + 25), 
        (12 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
        (12 * CELL_SIZE + 25, 9 * CELL_SIZE + 25),
        (6 * CELL_SIZE + 25, 9 * CELL_SIZE + 25),
        (6 * CELL_SIZE + 25, 14 * CELL_SIZE + 25), 
        (16 * CELL_SIZE + 25, 14 * CELL_SIZE + 25),
        (16 * CELL_SIZE + 25, 3 * CELL_SIZE + 25), 
        (18 * CELL_SIZE + 25, 3 * CELL_SIZE + 25),
    ],
    3: [
        (19 * CELL_SIZE + 25, 4 * CELL_SIZE + 25), 
        (12 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
        (12 * CELL_SIZE + 25, 12 * CELL_SIZE + 25),
        (6 * CELL_SIZE + 25, 12 * CELL_SIZE + 25),
        (6 * CELL_SIZE + 25, 5 * CELL_SIZE + 25), 
        (8 * CELL_SIZE + 25, 5 * CELL_SIZE + 25),
        (8 * CELL_SIZE + 25, 3 * CELL_SIZE + 25), 
        (4 * CELL_SIZE + 25, 3 * CELL_SIZE + 25),
        (4 * CELL_SIZE + 25, -1 * CELL_SIZE + 25),
    ],
    4: [
        (19 * CELL_SIZE, 14 * CELL_SIZE + 25), 
        (12 * CELL_SIZE + 25, 14 * CELL_SIZE + 25),
        (12 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
        (16 * CELL_SIZE + 25, 4 * CELL_SIZE + 25),
        (16 * CELL_SIZE + 25, 8 * CELL_SIZE + 25), 
        (4 * CELL_SIZE + 25, 8 * CELL_SIZE + 25),
        (4 * CELL_SIZE + 25, 3 * CELL_SIZE + 25), 
        (1 * CELL_SIZE + 25, 3 * CELL_SIZE + 25),
        (1 * CELL_SIZE + 25, -1 * CELL_SIZE + 25),
    ],
    5: [
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
}





# Classe Inimigo
class Enemy:
    def __init__(self, path, difficulty):
        self.path = path
        self.x, self.y = path[0]
        self.speed = 1
        self.health = 100
        self.current_point = 0
        self.difficulty = difficulty
        self.image = ENEMY_IMAGE_1 if difficulty == 1 else ENEMY_IMAGE_2 if difficulty == 2 else ENEMY_IMAGE_3
        self.flipped = False
        self.effect_index = 0
        self.effect_timer = 0

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

            # Verifica a direção do movimento e inverte a imagem se necessário
            if dx < 0 and not self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = True
            elif dx > 0 and self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False

    def draw(self):
        tower_rect = self.image.get_rect(center=(self.x, self.y))
        SCREEN.blit(self.image, tower_rect)
        # Barra de vida
        health_bar_length = 20
        health_ratio = self.health / (30 * 3)
        pygame.draw.rect(SCREEN, WHITE, (self.x - health_bar_length / 2, self.y - 15, health_bar_length, 5))
        pygame.draw.rect(SCREEN, (0, 255, 0), (self.x - health_bar_length / 2, self.y - 15, health_bar_length * health_ratio, 5))
        
        # Desenha o efeito de dano
        if self.effect_timer > 0:
            effect_image = EFFECT_IMAGES[self.effect_index]
            effect_rect = effect_image.get_rect(center=(self.x, self.y))
            SCREEN.blit(effect_image, effect_rect)
            self.effect_timer -= 1
            if self.effect_timer == 0:
                self.effect_index = (self.effect_index + 1) % len(EFFECT_IMAGES)

    def take_damage(self, damage, effect_index):
        self.health -= damage
        self.effect_timer = 5  # Duração do efeito de dano
        self.effect_index = effect_index  # Define o índice do efeito

# Classe Projectile
class Projectile:
    def __init__(self, x, y, target, damage, image, effect_index):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5
        self.image = image
        self.effect_index = effect_index

    def move(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < self.speed:
            self.target.take_damage(self.damage, self.effect_index)
            return True
        else:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed
            return False

    def draw(self):
        bullet_rect = self.image.get_rect(center=(self.x, self.y))
        SCREEN.blit(self.image, bullet_rect)

# Classe Torre
class Tower:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = {50: [0.425, 0.212, 0.111], 100: [1.2, 0.625, 0.312], 200: [1.7, 0.95, 0.65]}[cost]
        self.cost = cost
        self.cooldown = 60
        self.timer = 0
        self.image = TOWER_IMAGE_1 if cost == 50 else TOWER_IMAGE_2 if cost == 100 else TOWER_IMAGE_3
        self.angle = 0
        self.flipped = False
        self.projectiles = []
        self.projectile_image = BULLET_IMAGE_1 if cost == 50 else BULLET_IMAGE_2 if cost == 100 else BULLET_IMAGE_3
        self.effect_index = 0 if cost == 50 else 1 if cost == 100 else 2

    def attack(self, enemies):
        if self.timer == 0:
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if distance <= self.range:
                    self.projectiles.append(Projectile(self.x, self.y, enemy, self.damage[enemy.difficulty - 1] * 30, self.projectile_image, self.effect_index))
                    self.timer = self.cooldown
                    # Calculate angle to rotate the tower
                    dx, dy = enemy.x - self.x, enemy.y - self.y
                    self.angle = math.degrees(math.atan2(-dy, dx))  # Negative dy to correct the rotation direction
                    # Flip the image if it is upside down
                    if 90 < abs(self.angle) < 270:
                        if not self.flipped:
                            self.image = pygame.transform.flip(self.image, False, True)
                            self.flipped = True
                    else:
                        if self.flipped:
                            self.image = pygame.transform.flip(self.image, False, True)
                            self.flipped = False
                    return True
        return False

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        tower_rect = rotated_image.get_rect(center=(self.x, self.y))
        SCREEN.blit(rotated_image, tower_rect)  # Desenha a imagem da torre na posição correta
        
        for projectile in self.projectiles:
            projectile.draw()

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        self.projectiles = [p for p in self.projectiles if not p.move()]

# Funções auxiliares
BACKGROUND_IMAGE = pygame.image.load("assets/backgrounds/backgroundTowers.png")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (CELL_SIZE, CELL_SIZE))
PATH_BACKGROUND_IMAGE = pygame.image.load("assets/backgrounds/backgroundPath.png")
PATH_BACKGROUND_IMAGE = pygame.transform.scale(PATH_BACKGROUND_IMAGE, (CELL_SIZE, CELL_SIZE))

def draw_menu():
    menu_width = 200
    pygame.draw.rect(SCREEN, GRAY, (WIDTH - menu_width, 0, menu_width, HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Moedas: {player_money}", True, BLACK)
    SCREEN.blit(text, (WIDTH - menu_width + 10, 10))
    # Remove lives display
    # lives_text = font.render(f"Vidas: {lives}", True, BLACK)
    # SCREEN.blit(lives_text, (WIDTH - menu_width + 10, 50))

    for i, cost in enumerate(tower_costs):
        color = BLUE if cost == 50 else MAGENTA if cost == 100 else YELLOW if cost == 200 else CYAN
        tower_image = TOWER_IMAGE_1 if cost == 50 else TOWER_IMAGE_2 if cost == 100 else TOWER_IMAGE_3
        tower_rect = tower_image.get_rect(center=(WIDTH - menu_width // 1.3, 150 + i * 100))
        pygame.draw.rect(SCREEN, WHITE, tower_rect.inflate(10, 10), border_radius=5)  # Desenha um retângulo ao redor da torre
        SCREEN.blit(tower_image, tower_rect)
        cost_text = font.render(str(cost), True, BLACK)
        SCREEN.blit(cost_text, (tower_rect.right + 20, tower_rect.centery - cost_text.get_height() // 2))

def generate_enemies():
    global player_money, enemy_queue, enemy_spawn_timer  # Add this line to modify the global variable
    player_money = 300  # Reset player money at the start of each round
    f, m, d = qtdEnemysPerlevel[current_level]
    difficulty_counts = [(1, f), (2, m), (3, d)]
    enemy_list = []
    for difficulty, count in difficulty_counts:
        for _ in range(count):
            enemy_list.append(Enemy(pathLevels[current_level], difficulty))
    random.shuffle(enemy_list)  # Shuffle the enemies to randomize their order
    # Ensure the strongest enemy is not first
    if enemy_list and enemy_list[0].difficulty == 3:
        for i in range(1, len(enemy_list)):
            if enemy_list[i].difficulty != 3:
                enemy_list[0], enemy_list[i] = enemy_list[i], enemy_list[0]
                break
    enemy_queue = enemy_list  # Assign the shuffled list to enemy_queue
    enemy_spawn_timer = 0  # Reset the spawn timer

def draw_next_level_screen(level):
    SCREEN.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(f"NIVEL {level}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos

def wait_before_level_start():
    pygame.time.wait(5000)  # Espera 5 segundos

def is_cell_free(x, y):
    if x >= 18:  # Verifica se a célula está na área do menu
        return False
    for enemy in enemies:
        if enemy.x // CELL_SIZE == x and enemy.y // CELL_SIZE == y:
            return False
    for tower in towers:
        if tower.x // CELL_SIZE == x and tower.y // CELL_SIZE == y:
            return False
    path = pathLevels.get(current_level, [])
    for i in range(len(path) - 1):
        start_x, start_y = path[i]
        end_x, end_y = path[i + 1]
        if start_x == end_x:  # Vertical path
            if start_x // CELL_SIZE == x and min(start_y, end_y) // CELL_SIZE <= y <= max(start_y, end_y) // CELL_SIZE:
                return False
        elif start_y == end_y:  # Horizontal path
            if start_y // CELL_SIZE == y and min(start_x, end_x) // CELL_SIZE <= x <= max(start_x, end_x) // CELL_SIZE:
                return False
    return True

def draw_background():
    for x in range(0, WIDTH - 200, CELL_SIZE):  # Ajusta a largura da grade para 18 células
        for y in range(0, HEIGHT, CELL_SIZE):
            SCREEN.blit(BACKGROUND_IMAGE, (x, y))
    path = pathLevels.get(current_level, [])
    for i in range(len(path) - 1):
        start_x, start_y = path[i]
        end_x, end_y = path[i + 1]
        if start_x == end_x:  # Caminho vertical
            for y in range(min(start_y, end_y), max(start_y, end_y) + CELL_SIZE, CELL_SIZE):
                SCREEN.blit(PATH_BACKGROUND_IMAGE, (start_x - CELL_SIZE // 2, y - CELL_SIZE // 2))
        elif start_y == end_y:  # Caminho horizontal
            for x in range(min(start_x, end_x), max(start_x, end_x) + CELL_SIZE, CELL_SIZE):
                SCREEN.blit(PATH_BACKGROUND_IMAGE, (x - CELL_SIZE // 2, start_y - CELL_SIZE // 2))
    for x, y in path:
        SCREEN.blit(PATH_BACKGROUND_IMAGE, (x - CELL_SIZE // 2, y - CELL_SIZE // 2))

def draw_start_screen():
    SCREEN.fill(BLACK)
    # Remove the enemy images from the start screen
    # enemy_images = [ENEMY_IMAGE_1, ENEMY_IMAGE_2, ENEMY_IMAGE_3]
    # for x in range(0, WIDTH, 50):
    #     for y in range(0, HEIGHT, 50):
    #         enemy_image = random.choice(enemy_images)
    #         SCREEN.blit(enemy_image, (x, y))
    font = pygame.font.Font(None, 74)
    text = font.render("JOGAR", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(SCREEN, RED, text_rect.inflate(20, 20))  # Desenha um retângulo ao redor do texto
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    return text_rect  # Retorna o retângulo do botão

def draw_game_over_screen():
    SCREEN.fill(BLACK)
    font_main = pygame.font.Font(None, 74)
    font_sub = pygame.font.Font(None, 24)  # 33% do tamanho da frase principal
    phrases = [
        "TENTA DENOVO OUTRO DIA SEU RUIM",
        "É MAIS FACIL DESINSTALAR O JOGO",
        "TÁ JOGANDO COM O PÉ AMIGÃO?"
    ]
    main_text = font_main.render("VOCÊ PERDEU", True, RED)
    sub_text = font_sub.render(random.choice(phrases), True, RED)
    main_text_rect = main_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    sub_text_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    SCREEN.blit(main_text, main_text_rect)
    SCREEN.blit(sub_text, sub_text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos

def draw_pause_button():
    font = pygame.font.Font(None, 36)
    text = font.render("PAUSE", True, WHITE)
    text_rect = text.get_rect(topleft=(10, 10))
    pygame.draw.rect(SCREEN, RED, text_rect.inflate(20, 20))  # Desenha um retângulo ao redor do texto
    SCREEN.blit(text, text_rect)
    return text_rect  # Retorna o retângulo do botão

def draw_pause_screen():
    SCREEN.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("PAUSADO", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    SCREEN.blit(text, text_rect)
    font_small = pygame.font.Font(None, 36)
    continue_text = font_small.render("CONTINUAR", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    pygame.draw.rect(SCREEN, RED, continue_rect.inflate(20, 20))  # Desenha um retângulo ao redor do texto
    SCREEN.blit(continue_text, continue_rect)
    pygame.display.flip()
    return continue_rect  # Retorna o retângulo do botão

# Inicializar lista de inimigos, fila de inimigos e torres
enemies = []
enemy_queue = []
towers = []
enemy_spawn_timer = 0
spawn_interval = 30  # intervalo para cada inimigo aparecer
selected_tower_cost = None

# Variáveis para arrastar e soltar
dragging_tower = False
dragged_tower_cost = None
dragged_tower_image = None

# Variáveis de estado do jogo
running = True
game_started = False
game_over = False
paused = False

# Loop principal do jogo
while running:
    if not game_started:
        start_button_rect = draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    generate_enemies()  # Gerar inimigos ao iniciar o jogo
    elif game_over:
        draw_game_over_screen()
        game_over = False
        game_started = False
        player_points = 0
        player_money = 300  # Reset player money
        current_level = 1
        enemies = []
        enemy_queue = []
        towers = []
        enemy_spawn_timer = 0
    elif paused:
        continue_button_rect = draw_pause_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if continue_button_rect.collidepoint(mouse_x, mouse_y):
                    paused = False
    else:
        draw_background()  # Desenha o fundo das células das torres
        draw_decorations(current_level)  # Desenha as decorações para o nível atual
        path = pathLevels.get(current_level, [])  # Atualiza o caminho para o nível atual
        # Remova a linha preta no caminho do path
        # for i in range(len(path) - 1):
        #     pygame.draw.line(SCREEN, ROAD_COLOR, path[i], path[i + 1], 10)

        # Desenhar a grade e verificar eventos
        # Remova as linhas brancas que separam as células
        # for x in range(0, WIDTH - 200, CELL_SIZE):  # Ajusta a largura da grade para 18 células
        #     pygame.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT))
        # for y in range(0, HEIGHT, CELL_SIZE):
        #     pygame.draw.line(SCREEN, WHITE, (0, y), (WIDTH - 200, y))  # Ajusta a largura da grade para 18 células

        pause_button_rect = draw_pause_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pause_button_rect.collidepoint(mouse_x, mouse_y):
                    paused = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                if mouse_x > WIDTH - 200:
                    for i, cost in enumerate(tower_costs):
                        tower_rect = pygame.Rect(WIDTH - 200 + 50 - 15, 150 + i * 100 - 15, 30, 30)
                        if tower_rect.collidepoint(mouse_x, mouse_y) and player_money >= cost:
                            dragging_tower = True
                            dragged_tower_cost = cost
                            dragged_tower_image = TOWER_IMAGE_1 if cost == 50 else TOWER_IMAGE_2 if cost == 100 else TOWER_IMAGE_3

            if event.type == pygame.MOUSEBUTTONUP and dragging_tower:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

                if is_cell_free(grid_x, grid_y):
                    towers.append(Tower(grid_x * CELL_SIZE + 25, grid_y * CELL_SIZE + 25, dragged_tower_cost))
                    player_money -= dragged_tower_cost

                dragging_tower = False
                dragged_tower_cost = None
                dragged_tower_image = None

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
                player_money += reward_enemy[enemy.difficulty - 1]  # Add reward to player money
                enemies.remove(enemy)
            if enemy.current_point >= len(path) - 1:  # Inimigo chegou ao fim
                game_over = True
                enemies.remove(enemy)

        # Atualiza o spawn de inimigos
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= spawn_interval:
            if enemy_queue:
                enemies.append(enemy_queue.pop(0))
            elif not enemies and not enemy_queue:  # Todos os inimigos foram derrotados
                current_level += 1
                if current_level in pathLevels:
                    draw_next_level_screen(current_level)  # Exibe a tela de próximo nível
                    wait_before_level_start()  # Espera 5 segundos antes de iniciar o próximo nível
                    towers = []  # Remove todas as torres
                    generate_enemies()  # Gerar inimigos para o próximo nível
                else:
                    running = False  # Fim do jogo, todos os níveis completados
            enemy_spawn_timer = 0

        # Desenhar menu
        draw_menu()

        # Desenhar torre arrastada
        if dragging_tower and dragged_tower_image:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tower_rect = dragged_tower_image.get_rect(center=(mouse_x, mouse_y))
            SCREEN.blit(dragged_tower_image, tower_rect)

        pygame.display.flip()
        CLOCK.tick(FPS)

pygame.quit()
sys.exit()
