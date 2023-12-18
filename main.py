import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hopeless Death From Dropping Hazards")
BG = pygame.transform.scale(pygame.image.load('bg.jpg'), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_vel = 0

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 2

FONT = pygame.font.SysFont("aerial", 60)
FONT2 = pygame.font.SysFont("impact", 60)

yvel = -1
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0,0))
    time_text = FONT.render(f'Time survived: {round(elapsed_time)}s', 1, 'green')
    WIN.blit(time_text, (20,15))
    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, 'purple', star)
    pygame.display.update()

def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        global player_vel, yvel
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if player.y + yvel + PLAYER_HEIGHT > HEIGHT:
            yvel = 0
            player.y = HEIGHT - PLAYER_HEIGHT
        else:
            player.y += yvel
            yvel += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x - player_vel >= 0:
            player_vel -= 1
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player_vel + PLAYER_WIDTH <= WIDTH:
            player_vel += 1
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y == HEIGHT - PLAYER_HEIGHT:
            yvel -= 20

        player.x += player_vel
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        if star_count > star_add_increment:
            for _ in range(2):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT2.render(f"You Lost, Loser!", 1, "purple")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            break

        draw(player, elapsed_time, stars)
    pygame.quit()

if __name__ == "__main__": main()
