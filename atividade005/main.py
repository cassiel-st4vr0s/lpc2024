import pygame
import sys


# Classe Projectile
class Projectile:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 10)  # Projétil é um quadrado
        self.speed = 7
        self.direction = direction  # 1 = direita, -1 = esquerda

    def update(self):
        self.rect.x += self.speed * self.direction

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Projéteis são amarelos

    def is_off_screen(self, screen_width, screen_height):
        return (self.rect.right < 0 or self.rect.left > screen_width or
                self.rect.bottom < 0 or self.rect.top > screen_height)


# Classe Tank
class Tank:
    def __init__(self, x, y, color, is_player=True):
        self.rect = pygame.Rect(x, y, 50, 30)  # O tanque é um retângulo
        self.color = color
        self.speed = 5
        self.is_player = is_player
        self.cooldown = 0
        self.cooldown_time = 30  # tempo de recarga em frames

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def move(self, keys):
        if self.is_player:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < 800:  # largura da tela
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < 600:  # altura da tela
                self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = self.cooldown_time
            return Projectile(self.rect.centerx, self.rect.centery, 1 if self.is_player else -1)
        return None


# Função para detectar colisões
def check_collisions(projectiles, player_tank, enemy_tank):
    for projectile in projectiles[:]:
        if enemy_tank.rect.colliderect(projectile.rect):
            print("O tanque inimigo foi atingido!")
            continue

        if player_tank.rect.colliderect(projectile.rect):
            print("O tanque do jogador foi atingido!")


# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tank Game")

# Definindo cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Criando tanques
player_tank = Tank(100, SCREEN_HEIGHT // 2, WHITE)
enemy_tank = Tank(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2, (255, 0, 0))  # Tanque inimigo vermelho

# Taxa de disparo do inimigo
ENEMY_FIRE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_FIRE_EVENT, 2000)  # 2 segundos

projectiles = []

# Loop principal do jogo
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo do mouse
                new_projectile = player_tank.shoot()
                if new_projectile:
                    projectiles.append(new_projectile)
        if event.type == ENEMY_FIRE_EVENT:
            new_projectile = Projectile(enemy_tank.rect.centerx, enemy_tank.rect.centery, -1)
            if new_projectile:
                projectiles.append(new_projectile)

    # Lidar com pressionamento de teclas
    keys = pygame.key.get_pressed()
    player_tank.move(keys)

    # Atualizar objetos do jogo
    player_tank.update()
    enemy_tank.update()

    # Atualizar projéteis
    for projectile in projectiles[:]:
        projectile.update()
        if projectile.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
            projectiles.remove(projectile)

    # Verificar colisões
    check_collisions(projectiles, player_tank, enemy_tank)

    # Desenhar na tela
    screen.fill(BLACK)
    player_tank.draw(screen)
    enemy_tank.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)  # Desenhar projéteis que ainda estão ativos

    pygame.display.flip()
    clock.tick(60)  # FPS

pygame.quit()
sys.exit()
