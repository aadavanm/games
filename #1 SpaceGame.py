import pygame
import random
import json
import os

pygame.init()

# Window setup
WindowWidth = 1280
WindowHeight = 720
win = pygame.display.set_mode((WindowWidth, WindowHeight))
pygame.display.set_caption("Nebula Drift")
captionIcon = pygame.image.load("Images/captionIcon.png")
pygame.display.set_icon(captionIcon)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
SpaceBlack = (15, 15, 30)

# Images
Meteor = pygame.transform.scale(pygame.image.load("Images/meteorite.png"), (72, 72))
ShipImg = pygame.transform.rotate(pygame.image.load("Images/spaceship.png"), 45)
SpaceShip = pygame.transform.scale(ShipImg, (100, 100))
WreckImg = pygame.transform.scale(pygame.image.load("Images/wreck.png"), (64, 64))
Drone = pygame.transform.scale(pygame.image.load("Images/drone.png"), (72, 72))

# Load save data
save_file = "save_data.json"
if os.path.exists(save_file):
    with open(save_file, "r") as f:
        upgrade_data = json.load(f)
else:
    upgrade_data = {"max_health": 3}

# Player stats
ship_health = upgrade_data["max_health"]
ship_x = WindowWidth // 2
ship_y = WindowHeight - 100
ship_speed = 8
shield_active = False
shield_timer = 0
shield_uses = 3
screen_clear_text_timer = 0
bullet_cooldown = 0
start_time = pygame.time.get_ticks()
score = 0
smartbomb_uses = 1

# Game objects
asteroids = []
drones = []
wrecks = []
bullets = []

# Fonts
font = pygame.font.SysFont("arial", 28)

# Events
ASTEROID_SPAWN = pygame.USEREVENT + 1
DRONE_SPAWN = pygame.USEREVENT + 2
WRECK_SPAWN = pygame.USEREVENT + 3
pygame.time.set_timer(ASTEROID_SPAWN, 2000)
pygame.time.set_timer(DRONE_SPAWN, 4000)
pygame.time.set_timer(WRECK_SPAWN, 8000)

# Draw
def draw():
    win.fill(SpaceBlack)
    for asteroid in asteroids:
        win.blit(Meteor, asteroid)
    for drone in drones:
        win.blit(Drone, drone)
    for wreck in wrecks:
        win.blit(WreckImg, wreck)
    for bullet in bullets:
        pygame.draw.rect(win, (255, 255, 0), bullet)
    if shield_active:
        pygame.draw.circle(win, (0, 150, 255), (ship_x + 50, ship_y + 50), 60, 3)
    win.blit(SpaceShip, (ship_x, ship_y))

    # UI
    health_text = font.render(f"Health: {ship_health}", True, (255, 0, 0))
    win.blit(health_text, (20, 20))
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render(f"Time: {elapsed_time}s", True, (200, 200, 200))
    win.blit(time_text, (20, 60))
    score_text = font.render(f"Score: {score}", True, (0, 255, 0))
    win.blit(score_text, (20, 100))
    smartbomb_text = font.render(f"Smartbombs: {smartbomb_uses}", True, (255, 255, 0))
    win.blit(smartbomb_text, (20, 140))
    shield_text = font.render(f"Shields Left: {shield_uses}", True, (0, 200, 255))
    win.blit(shield_text, (20, 180))

    if screen_clear_text_timer > 0:
        clear_text = font.render("\U0001F4A3 Smartbomb Activated!", True, (255, 255, 0))
        win.blit(clear_text, (WindowWidth // 2 - 150, 50))

    if elapsed_time >= 120:
        win_text = font.render("\U0001F680 Hyperdrive Repaired! You Win!", True, (255, 255, 255))
        win.blit(win_text, (WindowWidth // 2 - 250, WindowHeight // 2))

# Game loop
running = True
while running:
    clock.tick(FPS)
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ASTEROID_SPAWN:
            asteroids.append([random.randint(0, WindowWidth - 72), -72])
        elif event.type == DRONE_SPAWN:
            drones.append([random.randint(0, WindowWidth - 72), -72])
        elif event.type == WRECK_SPAWN:
            wrecks.append([random.randint(0, WindowWidth - 64), -64])

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and ship_x > 0:
        ship_x -= ship_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and ship_x < WindowWidth - 100:
        ship_x += ship_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ship_y > 0:
        ship_y -= ship_speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and ship_y < WindowHeight - 100:
        ship_y += ship_speed
    if keys[pygame.K_j] and smartbomb_uses > 0:
        asteroids.clear()
        drones.clear()
        smartbomb_uses -= 1
        screen_clear_text_timer = 60

    if keys[pygame.K_r] and not shield_active and shield_uses > 0:
        shield_active = True
        shield_timer = pygame.time.get_ticks()
        shield_uses -= 1

    if keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bullets.append(pygame.Rect(ship_x + 45, ship_y, 10, 20))
        bullet_cooldown = 10

    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    if shield_active and pygame.time.get_ticks() - shield_timer > 5000:
        shield_active = False

    if screen_clear_text_timer > 0:
        screen_clear_text_timer -= 1

    for bullet in bullets[:]:
        bullet.y -= 12
        if bullet.y < 0:
            bullets.remove(bullet)

    ship_rect = pygame.Rect(ship_x, ship_y, 100, 100)
    for asteroid in asteroids[:]:
        asteroid[1] += 4
        if pygame.Rect(asteroid[0], asteroid[1], 72, 72).colliderect(ship_rect):
            if not shield_active:
                ship_health -= 1
            asteroids.remove(asteroid)

    for drone in drones[:]:
        drone[1] += 3
        if pygame.Rect(drone[0], drone[1], 72, 72).colliderect(ship_rect):
            if not shield_active:
                ship_health -= 1
            drones.remove(drone)

    for wreck in wrecks[:]:
        wreck[1] += 2
        if pygame.Rect(wreck[0], wreck[1], 64, 64).colliderect(ship_rect):
            wrecks.remove(wreck)
            upgrade_data["max_health"] = min(upgrade_data["max_health"] + 1, 5)
            ship_health = upgrade_data["max_health"]

    for bullet in bullets[:]:
        for drone in drones[:]:
            if bullet.colliderect(pygame.Rect(drone[0], drone[1], 72, 72)):
                if bullet in bullets:
                    bullets.remove(bullet)
                if drone in drones:
                    drones.remove(drone)
                    score += 1
                break

    if ship_health <= 0 or elapsed_time >= 120:
        running = False

    draw()
    pygame.display.update()

# Save upgrades
with open(save_file, "w") as f:
    json.dump(upgrade_data, f)

pygame.quit()
