import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Diyas!")

# Colors
WHITE = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# --- Load images ---
player_img = pygame.image.load("player.png").convert_alpha()
diya_img = pygame.image.load("diya.png").convert_alpha()

# Resize (optional)
player_img = pygame.transform.scale(player_img, (60, 60))
diya_img = pygame.transform.scale(diya_img, (40, 40))

# Player setup
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 5

# Diya setup
diyas = []  # list of tuples: (rect, spawn_time)
diya_duration = 3000  # ms = 3 seconds
last_spawn_time = 0
spawn_interval = 1500  # new diyas every 3 seconds

# Score
score = 0
font = pygame.font.Font(None, 36)

# Timer
game_duration = 60000  # 60 seconds
start_time = pygame.time.get_ticks()
game_over = False

# Game loop
running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()
    elapsed = current_time - start_time
    time_left = max(0, (game_duration - elapsed) // 1000)  # seconds remaining

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # --- Player movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += player_speed

        # Keep player inside screen
        player_rect.clamp_ip(screen.get_rect())

        # --- Spawn new diyas every 3s ---
        if current_time - last_spawn_time >= spawn_interval:
            for _ in range(2):  # spawn 2 diyas
                rect = diya_img.get_rect(
                    topleft=(random.randint(0, WIDTH - 40),
                             random.randint(0, HEIGHT - 40))
                )
                diyas.append((rect, current_time))
            last_spawn_time = current_time

        # --- Update diyas ---
        new_diyas = []
        for rect, spawn_time in diyas:
            if current_time - spawn_time > diya_duration:
                score -= 1  # missed it
            elif player_rect.colliderect(rect):
                score += 1  # collected
            else:
                new_diyas.append((rect, spawn_time))
        diyas = new_diyas

        # --- Timer check ---
        if elapsed >= game_duration:
            game_over = True

    # --- Drawing ---
    if not game_over:
        screen.blit(player_img, player_rect)
        for rect, _ in diyas:
            screen.blit(diya_img, rect)
        text = font.render(f"Score: {score}", True, TEXT_COLOR)
        time_text = font.render(f"Time Left: {time_left}s", True, TEXT_COLOR)
        screen.blit(text, (10, 10))
        screen.blit(time_text, (10, 50))
    else:
        # Game Over screen
        over_text = font.render("GAME OVER!", True, (200, 0, 0))
        final_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
        hint_text = font.render("Press R to restart or ESC to quit", True, TEXT_COLOR)
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        screen.blit(final_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(hint_text, (WIDTH // 2 - 180, HEIGHT // 2 + 20))

        # Restart or quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score = 0
            diyas = []
            start_time = pygame.time.get_ticks()
            game_over = False
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
