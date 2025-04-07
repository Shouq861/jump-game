import pygame
import sys

pygame.init()
pygame.mixer.init()

# إعداد الشاشة
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة زورو القفاز")

# الألوان
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# الخط
font = pygame.font.SysFont(None, 36)

# تحميل صورة الخلفية وتعديل حجمها
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# تحميل صورة اللاعب وتعديل حجمها
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

# تحميل صوت القفز
jump_sound = pygame.mixer.Sound("jump.wav")

# إعداد الأرض
ground_y = 350

clock = pygame.time.Clock()

def reset_game():
    global player_rect, obstacle, player_velocity, is_jumping, score, scored
    player_rect = player_image.get_rect()
    player_rect.topleft = (100, 300)

    obstacle = pygame.Rect(800, ground_y - 50, 50, 50)

    player_velocity = 0
    is_jumping = False
    score = 0
    scored = False

reset_game()
running = True
game_over = False

while running:
    screen.blit(background, (0, 0))  # رسم الخلفية

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # الضغط على زر المسافة أو الشاشة للقفز
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    player_velocity = -15
                    jump_sound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not is_jumping:
                    is_jumping = True
                    player_velocity = -15
                    jump_sound.play()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    game_over = False

    if not game_over:
        if is_jumping:
            player_rect.y += int(player_velocity)
            player_velocity += 0.8
            if player_rect.y >= ground_y - player_rect.height:
                player_rect.y = ground_y - player_rect.height
                is_jumping = False

        obstacle.x -= 5
        if obstacle.right < 0:
            obstacle.left = WIDTH
            scored = False

        if not scored and obstacle.right < player_rect.left:
            score += 1
            scored = True

        if player_rect.colliderect(obstacle):
            game_over = True

    # رسم الأرض
    pygame.draw.rect(screen, BROWN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    # رسم اللاعب والعقبة
    screen.blit(player_image, player_rect)
    pygame.draw.rect(screen, RED, obstacle)

    # رسم النقاط
    score_text = font.render("نقاطك: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # إذا خسر اللاعب
    if game_over:
        game_over_text = font.render("Game Over! نقاطك: " + str(score), True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 60))

        # زر إعادة اللعب
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, WHITE, restart_button)
        pygame.draw.rect(screen, BLACK, restart_button, 2)
        restart_text = font.render("أعد اللعب", True, BLACK)
        screen.blit(restart_text, (restart_button.x + 40, restart_button.y + 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()