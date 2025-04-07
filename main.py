import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة القفز")

WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

# تحميل صورة اللاعب
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))
player_rect = player_image.get_rect()
player_rect.topleft = (100, 300)

player_velocity = 0
is_jumping = False
gravity = 0.8

ground_y = 350

obstacle = pygame.Rect(800, ground_y - 50, 50, 50)
obstacle_speed = 5

score = 0
scored = False

clock = pygame.time.Clock()
running = True
jump_timer = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    jump_timer += clock.get_time()
    if jump_timer > 2000 and not is_jumping:
        is_jumping = True
        player_velocity = -15
        jump_timer = 0

    if is_jumping:
        player_rect.y += int(player_velocity)
        player_velocity += gravity
        if player_rect.y >= ground_y - player_rect.height:
            player_rect.y = ground_y - player_rect.height
            is_jumping = False

    obstacle.x -= obstacle_speed
    if obstacle.right < 0:
        obstacle.left = WIDTH
        scored = False

    if not scored and obstacle.right < player_rect.left:
        score += 1
        scored = True

    if player_rect.colliderect(obstacle):
        game_over_text = font.render("Game Over! نقاطك: " + str(score), True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue

    pygame.draw.rect(screen, BROWN, (0, ground_y, WIDTH, HEIGHT - ground_y))
    screen.blit(player_image, player_rect)
    pygame.draw.rect(screen, RED, obstacle)

    score_text = font.render("نقاطك: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()