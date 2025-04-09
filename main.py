# إضافة صورة وخصائص عنصر القوة
power_up_image = pygame.transform.scale(pygame.image.load("power_up.png"), (30, 30))
power_up_rect = pygame.Rect(WIDTH + 200, random.randint(100, 300), 30, 30)
has_power_up = False
power_up_start_time = 0

# داخل دالة reset_game
def reset_game():
    global power_up_rect, has_power_up, power_up_start_time
    power_up_rect = pygame.Rect(WIDTH + 200, random.randint(100, 300), 30, 30)
    has_power_up = False
    power_up_start_time = 0

# إضافة منطق لجمع عنصر القوة
if player_rect.colliderect(power_up_rect) and not has_power_up:
    has_power_up = True
    power_up_start_time = pygame.time.get_ticks()
    power_up_rect.x = -100

# رسم تأثير القوة
if has_power_up:
    for i in range(8):  # عدد الخطوط حول اللاعب
        color = random.choice([(255, 255, 0), (0, 255, 0), (255, 0, 255)])
        start_pos = player_rect.center
        angle = random.uniform(0, 2 * 3.14159)
        length = random.randint(30, 60)
        end_pos = (
            int(start_pos[0] + length * pygame.math.Vector2(1, 0).rotate_rad(angle).x),
            int(start_pos[1] + length * pygame.math.Vector2(1, 0).rotate_rad(angle).y),
        )
        pygame.draw.line(screen, color, start_pos, end_pos, 2)