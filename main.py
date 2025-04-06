import pygame
import sys

# تهيئة Pygame
pygame.init()

# إعدادات الشاشة
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة القفز")

# ألوان
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# إعداد اللاعب
player = pygame.Rect(100, 300, 50, 50)
player_velocity = 0
is_jumping = False
gravity = 0.8

# حلقة اللعبة
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # القفز
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_velocity = -15

    # فيزياء القفز
    if is_jumping:
        player.y += int(player_velocity)
        player_velocity += gravity
        if player.y >= 300:
            player.y = 300
            is_jumping = False

    # رسم اللاعب
    pygame.draw.rect(screen, BLUE, player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()