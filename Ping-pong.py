import pygame, sys, random
from datetime import datetime

pygame.init()

clock = pygame.time.Clock()

screen_width = 1280
screen_height = 760

screen = pygame.display.set_mode((screen_width, screen_height))
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)
font_large = pygame.font.SysFont('Arial', 66, bold=True)
#so i decided add classes for walls and ball, just because it was too messy
class Wall():
    def __init__(self, x, y, width, height, screen_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 0
        self.screen_height = screen_height

    def move(self):
        self.rect.y += self.speed
        #if hit the top, setting to the 0
        if self.rect.top <= 0:
            self.rect.top = 0
        #if hit bottom, setting to height coordinates
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)
class Ball:
        def __init__(self, x, y, width , height, speed_x, speed_y, screen_width, screen_height):
            self.score_1 = 0
            self.score_2 = 0
            self.rect = pygame.Rect(x,y , width, height)
            self.speed_x = speed_x
            self.speed_y = speed_y
            self.screen_width = screen_width
            self.screen_height = screen_height
        def physics(self, wall1, wall2):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            #check if hit the bottom or top
            if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
                 self.speed_y *=-1
            #check if hit left side or right side
            if self.rect.left <= 0:
                #adding score for left player
                self.score_2 +=1
                pygame.mixer.Sound('left.mp3').play()
                self.restart()
            if self.rect.right >= self.screen_width:
                #adding score for right player
                self.score_1+=1
                pygame.mixer.Sound('left.mp3').play()
                self.restart()
            #checking for collision with walls, then bounce back
            if self.rect.colliderect(wall1) or self.rect.colliderect(wall2):
                self.speed_x *=-1
                pygame.mixer.Sound('hit.mp3').play()
        #needed restart logic, so decided to put ball in the center every time he went out of screen
        def restart(self):
            self.rect.center = (screen_width / 2, screen_height/2)
            self.speed_y = 7 * random.choice((1, -1))
            self.speed_x = 7 * random.choice((1, -1))
        def draw_scores(self, screen):
            screen.blit(font_large.render(f"{self.score_1}", True, (255,255,255)),(300, 20))
            screen.blit(font_large.render(f"{self.score_2}", True, (255,255,255)),(800, 20))




ball = Ball(screen_width / 2- 15 , screen_height / 2 -15, 30, 30, 7, 7, screen_width, screen_height)
wall1 = Wall(screen_width - 20, screen_height / 2 - 70, 10, 140, screen_height)
wall2 = Wall(10, screen_height / 2 - 70, 10, 140, screen_height)
escape_pressed = True
paused = True
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED: # если наш юзерский, увеличваем скорость на 10 проц
            wall1.speed *= 1.1  
            wall2.speed *= 1.1
            ball.speed_x *= 1.1
            ball.speed_y *= 1.1
            #logic for walls movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                wall1.speed += 7
            if event.key == pygame.K_UP:
                wall1.speed -= 7
            if event.key == pygame.K_w:
                wall2.speed -= 7
            if event.key == pygame.K_s:
                wall2.speed += 7
            #also implemented pause f-n
            if event.key == pygame.K_ESCAPE:
                if not escape_pressed:
                    paused = not paused
                    escape_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                wall1.speed = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                wall2.speed = 0
            if event.key == pygame.K_ESCAPE:
                escape_pressed = False
    if not paused:
        wall1.move()
        wall2.move()
        ball.physics(wall1, wall2)
        screen.fill(bg_color)
        ball.draw_scores(screen)
        wall1.draw(screen, light_grey)
        wall2.draw(screen, light_grey)
        pygame.draw.ellipse(screen, light_grey, ball.rect)
        pygame.draw.line(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))
    else:
        screen.blit(font_large.render("PAUSE", True, pygame.Color('red')), (screen_width // 2 - 100, screen_height // 3))
    pygame.display.flip()
    clock.tick(60)

