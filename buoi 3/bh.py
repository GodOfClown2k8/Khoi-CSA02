import pygame
import random
import os
import logging

logging.basicConfig(filename='game.log', level=logging.DEBUG)

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ và các thông số khác
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60

# Kích thước hình ảnh sau khi giảm kích thước
SHIP_WIDTH, SHIP_HEIGHT = 40, 20
BULLET_WIDTH, BULLET_HEIGHT = 4, 8
TARGET_WIDTH, TARGET_HEIGHT = 40, 40

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Khởi tạo cửa sổ
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooting Game")

# Tải hình ảnh và thay đổi kích thước
def load_resources():
    try:
        background_image = pygame.image.load("background.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        ship_image = pygame.image.load("ship.jpg").convert_alpha()
        ship_image = pygame.transform.scale(ship_image, (SHIP_WIDTH, SHIP_HEIGHT))

        target_image = pygame.image.load("target.png").convert_alpha()
        target_image = pygame.transform.scale(target_image, (TARGET_WIDTH, TARGET_HEIGHT))

        bullet_image = pygame.image.load("bullet.png").convert_alpha()
        bullet_image = pygame.transform.scale(bullet_image, (BULLET_WIDTH, BULLET_HEIGHT))

        shoot_sound = pygame.mixer.Sound("gun-shots6-times-fast-230509.mp3")

        # Tải hình nền cho menu và pause screen
        menu_background = pygame.image.load("menu_background.jpg").convert()
        menu_background = pygame.transform.scale(menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        pause_background = pygame.image.load("pause_background.jpg").convert()
        pause_background = pygame.transform.scale(pause_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        return background_image, ship_image, target_image, bullet_image, shoot_sound, menu_background, pause_background
    except pygame.error as e:
        logging.error(f"Error loading resources: {e}")
        raise SystemExit("Error loading resources")

# Tạo lớp Ship
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
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
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
    
    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Tạo lớp Target
class Target(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(random.randint(0, WINDOW_WIDTH - TARGET_WIDTH), random.randint(-150, -50)))
        self.speed = 5
    
    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()
            new_target = target_pool.get_sprite()
            new_target.rect.topleft = (random.randint(0, WINDOW_WIDTH - TARGET_WIDTH), random.randint(-150, -50))
            all_sprites.add(new_target)
            targets.add(new_target)

# Object Pooling Class
class ObjectPool:
    def __init__(self, sprite_class, size, image):
        self.pool = pygame.sprite.Group()
        self.sprite_class = sprite_class
        self.size = size
        self.image = image
        self.populate()

    def populate(self):
        for _ in range(self.size):
            sprite = self.sprite_class(self.image)
            sprite.kill()  # Hide it initially
            self.pool.add(sprite)

    def get_sprite(self):
        if len(self.pool) == 0:
            self.populate()
        return self.pool.sprites()[0]

    def return_sprite(self, sprite):
        sprite.kill()
        self.pool.add(sprite)

# Khởi tạo các nhóm đối tượng và pools
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()

background_image, ship_image, target_image, bullet_image, shoot_sound, menu_background, pause_background = load_resources()

# Tạo pool cho mục tiêu
target_pool = ObjectPool(Target, 20, target_image)

# Tạo phi thuyền
ship = Ship(ship_image)
all_sprites.add(ship)

# Thêm các mục tiêu từ pool
for _ in range(20):
    target = target_pool.get_sprite()
    target.rect.topleft = (random.randint(0, WINDOW_WIDTH - TARGET_WIDTH), random.randint(-150, -50))
    all_sprites.add(target)
    targets.add(target)

# Khởi tạo điểm số và font
score = 0
highest_score = 0
font = pygame.font.SysFont(None, 36)

# Khởi tạo clock
clock = pygame.time.Clock()

def load_highest_score():
    global highest_score
    if os.path.isfile("highest_score.txt"):
        try:
            with open("highest_score.txt", "r") as file:
                highest_score = int(file.read())
        except ValueError as e:
            logging.error(f"Error reading highest score: {e}")
            highest_score = 0
    else:
        highest_score = 0

def save_highest_score():
    global highest_score
    try:
        with open("highest_score.txt", "w") as file:
            file.write(str(highest_score))
    except IOError as e:
        logging.error(f"Error saving highest score: {e}")

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))

def draw_highest_score():
    highest_score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    win.blit(highest_score_text, (10, 50))

def draw_pause_screen(selected_option):
    win.blit(pause_background, (0, 0))
    pause_text = font.render("PAUSED", True, WHITE)
    win.blit(pause_text, (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, WINDOW_HEIGHT // 3))
    draw_menu_buttons('pause', selected_option)

def draw_menu(selected_option):
    win.blit(menu_background, (0, 0))
    menu_title = pygame.font.SysFont(None, 72).render("Shooting Game", True, WHITE)
    win.blit(menu_title, (WINDOW_WIDTH // 2 - menu_title.get_width() // 2, WINDOW_HEIGHT // 4))
    draw_menu_buttons('main', selected_option)

def draw_menu_buttons(menu_type, selected_option):
    button_font = pygame.font.SysFont(None, 48)
    button_texts = {
        'main': ["Start", "Quit Game"],
        'pause': ["Back to Menu", "Quit Game"]
    }
    button_y = WINDOW_HEIGHT // 2 + 50

    for index, text in enumerate(button_texts[menu_type]):
        button_text = button_font.render(text, True, WHITE)
        button_rect = button_text.get_rect(center=(WINDOW_WIDTH // 2, button_y))
        # Đổi màu của nút khi được chọn
        if index == selected_option:
            pygame.draw.rect(win, BLUE, button_rect.inflate(20, 10))  # Nút được chọn
        else:
            pygame.draw.rect(win, BLACK, button_rect.inflate(20, 10))  # Nút không được chọn
        win.blit(button_text, button_rect)  # Vẽ chữ trên nút
        button_y += 60

def handle_menu_selection(selected_option, menu_type):
    if menu_type == 'main':
        if selected_option == 0:  # Start
            return 'game'
        elif selected_option == 1:  # Quit Game
            return 'quit'
    elif menu_type == 'pause':
        if selected_option == 0:  # Back to Menu
            return 'menu'
        elif selected_option == 1:  # Quit Game
            return 'quit'
    return None

def check_collisions():
    global score, highest_score

    # Va chạm giữa đạn và mục tiêu
    collisions = pygame.sprite.groupcollide(bullets, targets, True, True)
    if collisions:
        for _ in collisions:
            score += 10
            if score > highest_score:
                highest_score = score
                save_highest_score()

    return False

def game_loop():
    global score
    load_highest_score()
    running = True
    paused = False
    selected_option = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # Chuyển đổi trạng thái tạm dừng
                elif event.key == pygame.K_DOWN and paused:
                    selected_option = (selected_option + 1) % 2  # Di chuyển xuống
                elif event.key == pygame.K_UP and paused:
                    selected_option = (selected_option - 1) % 2  # Di chuyển lên
                elif event.key == pygame.K_RETURN and paused:
                    result = handle_menu_selection(selected_option, 'pause')
                    if result == 'menu':
                        return 'menu'
                    elif result == 'quit':
                        pygame.quit()
                        return 'quit'

        keys = pygame.key.get_pressed()
        
        if not paused:
            # Xử lý bắn đạn
            if keys[pygame.K_SPACE]:
                bullet = Bullet(ship.rect.centerx - BULLET_WIDTH // 2, ship.rect.top, bullet_image)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()  # Phát âm thanh bắn
            
            # Cập nhật tất cả các đối tượng
            all_sprites.update(keys)
            
            # Xử lý va chạm và cập nhật
            if check_collisions():
                return 'gameover'
        
        # Vẽ màn hình
        win.blit(background_image, (0, 0))  # Vẽ hình nền
        all_sprites.draw(win)
        draw_score()
        draw_highest_score()
        
        if paused:
            draw_pause_screen(selected_option)
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    menu = True
    selected_option = 0
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2  # Di chuyển xuống
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 2  # Di chuyển lên
                elif event.key == pygame.K_RETURN:
                    result = handle_menu_selection(selected_option, 'main')
                    if result == 'game':
                        menu = False
                        result = game_loop()
                        if result == 'gameover':
                            score = 0
                            menu = True
                    elif result == 'quit':
                        pygame.quit()
                        return

        # Vẽ menu
        draw_menu(selected_option)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        pygame.quit()
