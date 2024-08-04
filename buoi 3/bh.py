import pygame
import random
import os
import logging

logging.basicConfig(filename='game.log', level=logging.DEBUG)

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
SHIP_WIDTH, SHIP_HEIGHT = 50, 30
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
TARGET_WIDTH, TARGET_HEIGHT = 50, 50
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Khởi tạo cửa sổ
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")

# Chèn ảnh 
try:
    ship_image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT))
    ship_image.fill(BLUE)  # Thay thế bằng hình chữ nhật xanh cho phi thuyền
    target_image = pygame.Surface((TARGET_WIDTH, TARGET_HEIGHT))
    target_image.fill(RED)  # Thay thế bằng hình chữ nhật đỏ cho mục tiêu
except pygame.error as e:
    logging.error(f"Error creating surface: {e}")
    raise SystemExit("Error creating surfaces")

# Tạo lớp Ship
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_image
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.speed = 5
    
    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        
        # Đảm bảo phi thuyền không ra ngoài màn hình
        self.rect.x = max(0, min(WINDOW_WIDTH - SHIP_WIDTH, self.rect.x))
        self.rect.y = max(0, min(WINDOW_HEIGHT - SHIP_HEIGHT, self.rect.y))

# Tạo lớp Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
    
    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Tạo lớp Target
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = target_image
        self.rect = self.image.get_rect(topleft=(random.randint(0, WINDOW_WIDTH - TARGET_WIDTH), random.randint(-150, -50)))
        self.speed = 3
    
    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            # Re-create target if it goes off screen
            new_target = Target()
            all_sprites.add(new_target)
            targets.add(new_target)

# Tạo lớp Asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_WIDTH, ASTEROID_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(random.randint(0, WINDOW_WIDTH - ASTEROID_WIDTH), random.randint(-200, -50)))
        self.speed = 3
    
    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            # Re-create asteroid if it goes off screen
            new_asteroid = Asteroid()
            all_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)

# Khởi tạo các nhóm đối tượng
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Tạo các đối tượng
ship = Ship()
all_sprites.add(ship)

for _ in range(5):
    target = Target()
    all_sprites.add(target)
    targets.add(target)

for _ in range(3):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Khởi tạo điểm số
score = 0
highest_score = 0
font = pygame.font.SysFont(None, 36)

# Khởi tạo clock
clock = pygame.time.Clock()

def load_highest_score():
    global highest_score
    if os.path.isfile("highest_score.txt"):
        with open("highest_score.txt", "r") as file:
            highest_score = int(file.read())
    else:
        highest_score = 0

def save_highest_score():
    global highest_score
    with open("highest_score.txt", "w") as file:
        file.write(str(highest_score))

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))

def draw_highest_score():
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    win.blit(highest_score_text, (10, 50))

def draw_pause_screen():
    pause_text = font.render("PAUSED - Press 'P' to Resume", True, BLACK)
    win.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, WINDOW_HEIGHT // 2 - pause_text.get_height() // 2))

def check_collisions():
    global score, highest_score

    # Va chạm giữa đạn và mục tiêu
    for bullet in bullets:
        target_hit_list = pygame.sprite.spritecollide(bullet, targets, True)
        for target in target_hit_list:
            bullet.kill()
            score += 10
            new_target = Target()
            all_sprites.add(new_target)
            targets.add(new_target)

    # Va chạm giữa phi thuyền và thiên thạch
    if pygame.sprite.spritecollideany(ship, asteroids):
        if score > highest_score:
            highest_score = score
        save_highest_score()
        return True

    return False

def main():
    global score
    load_highest_score()
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_p]:
            paused = not paused

        if not paused:
            # Xử lý bắn đạn
            if keys[pygame.K_SPACE]:
                bullet = Bullet(ship.rect.centerx - BULLET_WIDTH // 2, ship.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            
            # Cập nhật tất cả các đối tượng
            all_sprites.update(keys)
            
            # Xử lý va chạm và cập nhật
            if check_collisions():
                break
        
        # Vẽ màn hình
        win.fill(WHITE)
        all_sprites.draw(win)
        draw_score()
        draw_highest_score()
        
        if paused:
            draw_pause_screen()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        pygame.quit()
