import pygame
import os
import random
pygame.font.init()

from player import Player
from enemy import Enemy

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH,HEIGHT))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("century",50)
    lost_font = pygame.font.SysFont("comicsans",70)

    enemies = []
    wave_length = 5
    enemy_vel = 2
    
    player_vel = 5
    laser_vel = 10

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        #draw window
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Vidas: {lives}", 1 , (255,255,255))
        level_label = main_font.render(f"Nivel: {level}", 1 , (255,255,255))
        
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("¡Perdiste!", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()
    

    while run:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            lives -= 1
            player.health = 100

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                run = False
            else:
                continue
        
        #add enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player, HEIGHT)

            if  random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            

        player.move_lasers(-laser_vel, enemies, HEIGHT)

        
def main_menu():
    title_font = pygame.font.SysFont("century", 70)
    subtitle_font = pygame.font.SysFont("century", 40)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label1 = subtitle_font.render("haga clic para comenzar", 1, (255,255,255))
        WIN.blit(title_label1, (WIDTH/2 - title_label1.get_width()/2, 350))
        title_label2 = title_font.render("INVASORES DEL ESPACIO", 1, (255,255,255))
        WIN.blit(title_label2, (WIDTH/2 - title_label2.get_width()/2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
