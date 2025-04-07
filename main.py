import pygame
import random

# تهيئة Pygame
pygame.init()

# أبعاد الشاشة
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة قفز البنات")

# الألوان
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# الخط
font = pygame.font.SysFont(None, 36)

# تحميل صورة الخلفية
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# تحميل صورة اللاعب
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

# تحميل صور العقبات
obstacle_images = [
    pygame.transform.scale(pygame.image.load("crate.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("chest.png"), (50, 50)),
]

# تحميل صوت القفز (اختياري)
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
except:
    jump_sound = None

# إعداد الأرض
ground_y = 350

# إعداد اللاعب
player_x = 100
player_y = ground_y
player_velocity = 0
gravity = 1
jump_strength = -15
is_jumping = False

# إعداد العقبات
obstacles = []
obstacle_speed = 5
spawn_obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_obstacle_event, 1500)

# النقاط
score = 0

# حلقة اللعبة
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))

    # الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_obstacle_event:
            image = random.choice(obstacle_images)
            rect = image.get_rect(midbottom=(WIDTH, ground_y))
            obstacles.append((image, rect))

    # تحكم اللاعب
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity = jump_strength
        is_jumping = True
        if jump_sound:
            jump_sound.play()

    # تحديث موقع اللاعب
    player_velocity += gravity
    player_y += player_velocity
    if player_y >= ground_y:
        player_y = ground_y
        is_jumping = False

    # رسم اللاعب
    screen.blit(player_image, (player_x, player_y))

    # تحديث العقبات
    for obstacle in obstacles[:]:
        obstacle[1].x -= obstacle_speed
        screen.blit(obstacle[0], obstacle[1])

        # تصادم
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        if player_rect.colliderect(obstacle[1]):
            running = False

        # تخطي العقبة
        if obstacle[1].x + 50 < player_x and not hasattr(obstacle[1], 'counted'):
            score += 1
            setattr(obstacle[1], 'counted', True)

    # رسم النقاط
    score_text = font.render(f"النقاط: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()