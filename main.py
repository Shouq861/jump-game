import pygame "
import sys
import random

pygame.init()
pygame.mixer.init()


# إعداد الشاشة
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zorro Jump Game - Basic Power-up")

# الألوان
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# الخط
font = pygame.font.SysFont(None, 36)

# تحميل الصور
background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
player_image_original = pygame.transform.scale(pygame.image.load("player.png"), (50, 50))
obstacle_images = [
    pygame.transform.scale(pygame.image.load("crate.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("chest.png"), (50, 50)),
]
power_up_image = pygame.transform.scale(pygame.image.load("power_up.png"), (30, 30))

# الأصوات
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
except:
    jump_sound = None
try:
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    crash_sound = None

# الإعدادات
ground_y = 350
clock = pygame.time.Clock()
POWER_UP_DURATION = 5000  # مدة تأثير عنصر القوة بالميلي ثانية

def reset_game():
    global player_rect, player_velocity, is_jumping, score, scored
    global obstacle_rect, obstacle_image, obstacle_speed
    global power_up_rect, has_power_up, power_up_start_time
    global difficulty_level, game_over, player_image

    player_image = player_image_original.copy()
    player_rect = player_image.get_rect(topleft=(100, 300))

    obstacle_image = random.choice(obstacle_images)
    obstacle_rect = pygame.Rect(800, ground_y - 50, 50, 50)

    power_up_rect = pygame.Rect(WIDTH + 200, random.randint(100, 300), 30, 30)
    has_power_up = False
    power_up_start_time = 0

    player_velocity = 0
    is_jumping = False
    score = 0
    scored = False
    difficulty_level = 1
    obstacle_speed = 5
    game_over = False

reset_game()
running = True

while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_jumping:
                    is_jumping = True
                    player_velocity = -15
                    if jump_sound:
                        jump_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not is_jumping:
                    is_jumping = True
                    player_velocity = -15
                    if jump_sound:
                        jump_sound.play()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    reset_game()
    
    if not game_over:
        # زيادة الصعوبة تدريجيًا
        if score % 10 == 0 and score > 0:
            difficulty_level = score // 10 + 1
        obstacle_speed = 5 + difficulty_level

        # حركة اللاعب
        if is_jumping:
            player_image.set_alpha(150)
            player_rect.y += int(player_velocity)
            player_velocity += 0.8
            if player_rect.y >= ground_y - player_rect.height:
                player_rect.y = ground_y - player_rect.height
                is_jumping = False
        else:
            player_image.set_alpha(255)

        # حركة العقبة
        obstacle_rect.x -= obstacle_speed
        if obstacle_rect.right < 0:
            obstacle_rect.left = WIDTH
            obstacle_image = random.choice(obstacle_images)
            scored = False

        # حركة عنصر القوة
        if not has_power_up:
            power_up_rect.x -= 5
            if power_up_rect.right < 0:
                power_up_rect.left = WIDTH + random.randint(100, 300)
                power_up_rect.y = random.randint(100, 300)
        else:
            if pygame.time.get_ticks() - power_up_start_time > POWER_UP_DURATION:
                has_power_up = False

        # جمع عنصر القوة
        if player_rect.colliderect(power_up_rect) and not has_power_up:
            has_power_up = True
            power_up_start_time = pygame.time.get_ticks()
            power_up_rect.x = -100  # إخفاء العنصر بعد الجمع

        # تسجيل النقاط
        if not scored and obstacle_rect.right < player_rect.left:
            score += 1
            scored = True

        # التصادم: إذا لم يكن عنصر القوة مفعل
        if not has_power_up and player_rect.colliderect(obstacle_rect):
            if crash_sound:
                crash_sound.play()
            game_over = True
            for _ in range(5):
                screen.fill(random.choice([BROWN, BLACK]))
                pygame.display.flip()
                pygame.time.delay(30)

    # رسم الأرض
    pygame.draw.rect(screen, BROWN, (0, ground_y, WIDTH, HEIGHT - ground_y))
    
    # رسم اللاعب
    screen.blit(player_image, player_rect)
    
    # رسم تأثير الشعاع عند تفعيل عنصر القوة (8 خطوط)
    if has_power_up:
        for i in range(8):
            color = random.choice([(255, 255, 0), (0, 255, 0), (255, 0, 255)])
            start_pos = player_rect.center
            angle = random.uniform(0, 2 * 3.14159)
            length = random.randint(30, 60)
            end_pos = (
                int(start_pos[0] + length * pygame.math.Vector2(1, 0).rotate_rad(angle).x),
                int(start_pos[1] + length * pygame.math.Vector2(1, 0).rotate_rad(angle).y),
            )
            pygame.draw.line(screen, color, start_pos, end_pos, 2)
    
    # رسم العقبة وعنصر القوة
    screen.blit(obstacle_image, obstacle_rect)
    if not has_power_up:
        screen.blit(power_up_image, power_up_rect)
    
    # عرض النقاط
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # شاشة نهاية اللعبة
    if game_over:
        game_over_text = font.render(f"Game Over! Your Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 60))
        
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, WHITE, restart_button)
        pygame.draw.rect(screen, BLACK, restart_button, 2)
        restart_text = font.render("Restart", True, BLACK)
        screen.blit(restart_text, (restart_button.x + 40, restart_button.y + 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()