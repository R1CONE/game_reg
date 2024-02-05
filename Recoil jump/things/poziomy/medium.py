import pygame
import sys
import math
import os
import random

# Inicjalizacja Pygame
pygame.init()

# Inicjalizacja Pygame Mixer
pygame.mixer.init()

# Wczytanie dźwięków
shoot_sound = pygame.mixer.Sound("things/sounds/shoot.mp3")
die_sound = pygame.mixer.Sound("things/sounds/die.mp3")
point_sound = pygame.mixer.Sound("things/sounds/point.mp3")

# Ustawianie głośności dla poszczególnych dźwięków
shoot_sound.set_volume(1.0)  # Ustaw głośność strzału na 100%
die_sound.set_volume(1.0)    # Ustaw głośność dźwięku śmierci na 100%
point_sound.set_volume(1.0)  # Ustaw głośność dźwięku punktu na 100%

# Ustawienia okna gry
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Ustaw tryb windowed fullscreen
width, height = screen.get_size()  # Pobierz rozmiary okna
pygame.display.set_caption("Recoil Jump 2 made by @werbel")

# Kolor granic okna
border_color = (0, 0, 0)
border_thickness = 5

# Load bullet image
bullet_image = pygame.image.load("things/graphics/bullet.png").convert_alpha()
bullet_size = (30, 30)  # Nowy rozmiar strzały
bullet_image = pygame.transform.scale(bullet_image, bullet_size)

# Gracz (strzelba)
shotgun_images = [
    pygame.image.load("things/graphics/shotgun.png").convert_alpha(),
    pygame.image.load("things/graphics/shotgun2.png").convert_alpha()
]
current_shotgun_image = shotgun_images[0]
player_original_rect = current_shotgun_image.get_rect(center=(width // 2, height // 2))
player_size = (50, 50)  # Nowy rozmiar postaci
player_rect = pygame.Rect(player_original_rect.topleft, player_size)
player_speed = 5
player_velocity = [0, 0]
is_player_alive = True

# Grawitacja
gravity = 0.5

# Strzały
bullet_speed = 5
bullets = []

# Zmienna do śledzenia stanu strzałby
shotgun_state = 0  # 0 - shotgun1.png, 1 - shotgun2.png
last_shot_time = 0
shotgun_switch_duration = 100  # Czas trwania zmiany strzałby w milisekundach

# Zbieralne punkty
points = []
point_radius = 10
point_respawn_time = 50  # Czas respawnu punktów w klatkach
last_point_spawn_time = 0
points_collected = 0  # Licznik zebranych punktów

# Spadające kamienie
stones = []
stone_texture = pygame.image.load("things/graphics/stone.png").convert_alpha()  # Tekstura kamienia
stone_size = (10, 10)
stone_speed = 7  # Zwiększona prędkość kamieni
stone_respawn_time = 600  # Czas respawnu kamienia w klatkach
last_stone_spawn_time = 0

# Kolor czcionki
font_color = (0, 0, 0)

# Funkcja odrodzenia gracza
def respawn_player():
    global player_rect, player_velocity, is_player_alive, bullets, shotgun_state, current_shotgun_image
    player_rect.center = (width // 2, height // 2)
    player_velocity = [0, 0]
    is_player_alive = True
    bullets.clear()
    shotgun_state = 0
    current_shotgun_image = shotgun_images[shotgun_state]

def draw_hitboxes():
    # Draw hitbox for the player (strzelba)
    pygame.draw.rect(screen, (0, 255, 0), player_rect, 2)

    # Draw hitbox for each point
    for point in points:
        point_rect = pygame.Rect(point[0] - point_radius, point[1] - point_radius, point_radius * 2, point_radius * 2)
        pygame.draw.rect(screen, (255, 0, 0), point_rect, 2)

    # Draw hitbox for each stone
    for stone in stones:
        pygame.draw.rect(screen, (0, 0, 255), stone, 2)

# Funkcja respawnu punktów
def respawn_points():
    global points, last_point_spawn_time, points_collected
    points_collected += 1
    points.clear()
    x = random.randint(width // 2 - 100, width // 2 + 100)  # Losowa pozycja X w okolicach środka ekranu
    y = random.randint(height // 2 - 100, height // 2 + 100)  # Losowa pozycja Y w okolicach środka ekranu
    points.append((x, y))

    last_point_spawn_time = pygame.time.get_ticks()

# Funkcja respawnu kamienia
def respawn_stone():
    global stones, last_stone_spawn_time
    stones.clear()
    
    num_stones = 2  # Nowa liczba kamieni
    
    for _ in range(num_stones):
        # Maksymalne odległości od środka kamienia w poziomie i w pionie
        max_offset_x = max(0, (stone_size[0] - 50) // 2)
        max_offset_y = max(0, (stone_size[1] - 29) // 2)
        
        offset_x = random.randint(0, max_offset_x)
        offset_y = random.randint(0, max_offset_y)
        
        x = random.randint(0, width - stone_size[0])  # Losowa pozycja X w obszarze ekranu
        y = -stone_size[1]  # Początkowa pozycja Y na górze ekranu
        
        stone_rect = pygame.Rect(x + offset_x, y + offset_y, 50, 29)
        stones.append(stone_rect)

    last_stone_spawn_time = pygame.time.get_ticks()

# Funkcja sprawdzająca kolizję kamienia z graczem
def check_stone_collision(player_rect, stone_rect):
    return player_rect.colliderect(stone_rect)

# Funkcja rysująca punkty
def draw_points():
    for point in points:
        pygame.draw.circle(screen, (255, 0, 0), (int(point[0]), int(point[1])), point_radius)

# Funkcja rysująca kamienie
def draw_stones():
    for stone in stones:
        screen.blit(stone_texture, stone.topleft)
        pygame.draw.rect(screen, (0, 0, 255), stone, 2)

# Funkcja rysująca komunikat po śmierci
def draw_death_message():
    font = pygame.font.Font(None, 36)
    text = font.render("Kliknij R, aby się odrodzić", True, font_color)
    text_rect = text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(text, text_rect)

# Funkcja rysująca licznik punktów
def draw_points_counter():
    font = pygame.font.Font(None, 30)
    text = font.render(f"Punkty: {points_collected}", True, font_color)
    screen.blit(text, (10, 10))

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not is_player_alive:
                respawn_player()
                respawn_points()
                respawn_stone()
                points_collected = 0
                die_sound.stop()  # Zatrzymaj dźwięk śmierci przy respawnie

        elif event.type == pygame.MOUSEBUTTONDOWN and is_player_alive:
            # Oblicz kąt pomiędzy graczem a myszką
            angle = math.atan2(pygame.mouse.get_pos()[1] - player_rect.centery,
                               pygame.mouse.get_pos()[0] - player_rect.centerx)
            # Dodaj strzał z odpowiednią prędkością w kierunku myszki
            bullet = [player_rect.centerx, player_rect.centery, bullet_speed * math.cos(angle),
                      bullet_speed * math.sin(angle)]
            bullets.append(bullet)

            # Odtwórz dźwięk strzału
            shoot_sound.play()

            # Zmiana wyglądu strzałby
            shotgun_state = 1
            current_shotgun_image = shotgun_images[shotgun_state]
            last_shot_time = pygame.time.get_ticks()

            # Dodaj odrzut gracza po strzale
            recoil_speed = 10
            player_velocity[0] -= recoil_speed * math.cos(angle)
            player_velocity[1] -= recoil_speed * math.sin(angle)

    # Ruch gracza
    if is_player_alive:
        # Zastosowanie grawitacji
        player_velocity[1] += gravity

        player_rect.x += player_velocity[0]
        player_rect.y += player_velocity[1]

        # Sprawdzenie kolizji z krawędziami ekranu
        if player_rect.left < 0 or player_rect.right > width or player_rect.top < 0 or player_rect.bottom > height:
            is_player_alive = False
            die_sound.play()  # Dodaj odtwarzanie dźwięku śmierci

        # Hamowanie prędkości gracza (dodaj własne wartości tarcia)
        player_velocity[0] *= 0.9
        player_velocity[1] *= 0.9

        # Sprawdzanie kolizji z punktami
        if points and check_stone_collision(player_rect, pygame.Rect(points[0][0] - point_radius, points[0][1] - point_radius, point_radius * 2, point_radius * 2)):
            respawn_points()

        # Sprawdzanie kolizji z kamieniami
        for stone in stones:
            if check_stone_collision(player_rect, stone):
                is_player_alive = False
                die_sound.play()

    # Ruch strzałów
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    # Ruch kamieni
    for stone in stones:
        stone.y += stone_speed

        # Sprawdzenie kolizji kamienia z dolną krawędzią ekranu
        if stone.bottom >= height:
            stones.remove(stone)
            respawn_stone()

    # Obrót gracza w kierunku myszki
    if is_player_alive:
        angle_to_mouse = -math.atan2(pygame.mouse.get_pos()[1] - player_rect.centery,
                                     pygame.mouse.get_pos()[0] - player_rect.centerx)
        rotated_player = pygame.transform.rotate(current_shotgun_image, math.degrees(angle_to_mouse))
        player_rect = rotated_player.get_rect(center=player_rect.center)

    # Sprawdzenie czasu trwania zmiany strzałby
    if pygame.time.get_ticks() - last_shot_time > shotgun_switch_duration:
        shotgun_state = 0
        current_shotgun_image = shotgun_images[shotgun_state]

    # Sprawdzanie czasu respawnu punktów
    if not points and points_collected < 5:  # Tworzymy nowy punkt tylko jeśli nie ma żadnych punktów i zebrano mniej niż 5
        if pygame.time.get_ticks() - last_point_spawn_time > point_respawn_time:
            respawn_points()

    # Sprawdzanie czasu respawnu kamieni
    if not stones:
        if pygame.time.get_ticks() - last_stone_spawn_time > stone_respawn_time:
            respawn_stone()

    # Rysowanie tła
    screen.fill((255, 255, 255))

    # Rysowanie gracza
    if is_player_alive:
        screen.blit(rotated_player, player_rect.topleft)
    else:
        draw_death_message()

    # Rysowanie punktów
    draw_points()

    # Rysowanie kamieni
    draw_stones()

    # Rysowanie licznika punktów
    draw_points_counter()

    # Rysowanie strzałów
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[:2], bullet_size)
        screen.blit(pygame.transform.scale(bullet_image, bullet_size), bullet_rect)

    # Rysowanie hitboxów
    draw_hitboxes()

    # Wyświetlanie okna
    pygame.display.flip()

    # Kontrola liczby klatek
    pygame.time.Clock().tick(60)