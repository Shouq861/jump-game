import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة القفز")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

# اللاعب
player = pygame.Rect(100, 300, 50, 50)
player_velocity = 0
is_jumping = False
gravity = 0.8

# الأرض
ground_y = 350

# العقبة
obstacle = pygame.Rect(800, ground_y - 50, 50, 50)
obstacle_speed = 5

# النقاط
score = 0
scored = False  # عشان ما يحسب النقطة مرتين

clock = pygame.time.Clock()
running = True
jump_timer = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # القفز التلقائي
    jump_timer += clock.get_time()
    if jump_timer > 2000 and not is_jumping:
        is_jumping = True
        player_velocity = -15
        jump_timer = 0

    # القفز
    if is_jumping:
        player.y += int(player_velocity)
        player_velocity += gravity
        if player.y >= ground_y - player.height:
            player.y = ground_y - player.height
            is_jumping = False

    # تحريك العقبة
    obstacle.x -= obstacle_speed
    if obstacle.right < 0:
        obstacle.left = WIDTH
        scored = False  # جاهز لحساب نقطة جديدة

    # حساب النقاط
    if not scored and obstacle.right < player.left:
        score += 1
        scored = True

    # كشف الاصطدام
    if player.colliderect(obstacle):
        # شاشة Game Over
        game_over_text = font.render("Game Over! نقاطك: " + str(score), True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue

    # رسم الأرض
    pygame.draw.rect(screen, BROWN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    # رسم اللاعب والعقبة
    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, obstacle)

    # عرض النقاط
    score_text = font.render("نقاطك: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()