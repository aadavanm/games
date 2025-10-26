import pygame
import random

# Initialize
pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run from the Rain")
clock = pygame.time.Clock()

# Load background
background_img = pygame.image.load("bg.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load sounds
rain_sound = pygame.mixer.Sound("rain_sound.mp3")
thunder_sound = pygame.mixer.Sound("thunder.wav")
hit_sound = pygame.mixer.Sound("hit_sound.wav")

rain_sound.play(-1)  # loop forever

# Colors
WHITE = (255, 255, 255)
BLUE = (255, 255, 0)
GRAY = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

# Font
font = pygame.font.SysFont("Arial", 24)

# Player
player_img = pygame.image.load("diya.png").convert_alpha()
player_rect = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
player_speed = 6

# Umbrella visual
umbrella_img = pygame.Surface((40, 20))
umbrella_img.fill(YELLOW)

# Game variables
lives = 3

raindrops = []
drop_speed = 6
drop_interval = 15
frame_count = 0

# Umbrella power-up logic
umbrella_item = None
umbrella_timer = 0
umbrella_active = False
umbrella_duration = 5000  # 5 seconds
next_umbrella_spawn = random.randint(400, 800)

# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))
    frame_count += 1
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Spawn raindrops
    if frame_count % drop_interval == 0:
        x = random.randint(0, WIDTH)
        drop = pygame.Rect(x, 0, 5, 15)
        raindrops.append(drop)

    # Move and draw raindrops
    for drop in raindrops[:]:
        drop.y += drop_speed
        pygame.draw.rect(screen, BLUE, drop)

        if drop.colliderect(player_rect):
            if not umbrella_active:
                lives -= 1
                hit_sound.play()
                raindrops.remove(drop)
                if lives <= 0:
                    print("Game Over")
                    running = False
            else:
                raindrops.remove(drop)

        elif drop.y > HEIGHT:
            raindrops.remove(drop)

    # Spawn umbrella item
    if not umbrella_item and frame_count % next_umbrella_spawn == 0:
        umbrella_x = random.randint(50, WIDTH - 50)
        umbrella_item = pygame.Rect(umbrella_x, 0, 30, 30)

    # Move and draw umbrella item
    if umbrella_item:
        umbrella_item.y += 3
        pygame.draw.rect(screen, YELLOW, umbrella_item)

        if umbrella_item.colliderect(player_rect):
            umbrella_active = True
            umbrella_timer = current_time
            umbrella_item = None
            next_umbrella_spawn = frame_count + random.randint(400, 800)

        elif umbrella_item.y > HEIGHT:
            umbrella_item = None

    # Deactivate umbrella after 5 sec
    if umbrella_active and current_time - umbrella_timer > umbrella_duration:
        umbrella_active = False

    # Thunder chance
    if random.randint(0, 800) == 1:
        thunder_sound.play()

    # Draw player
    screen.blit(player_img, player_rect)

    # Draw umbrella over player
    if umbrella_active:
        umbrella_pos = (player_rect.centerx - 20, player_rect.top - 20)
        screen.blit(umbrella_img, umbrella_pos)

    # Display lives
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(lives_text, (10, 10))

    if umbrella_active:
        screen.blit(font.render("☂️ Umbrella Active", True, GREEN), (10, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()