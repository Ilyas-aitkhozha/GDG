import pygame, sys

pygame.init()

clock = pygame.time.Clock()

screen_width = 1360
screen_height = 930

screen = pygame.display.set_mode((screen_width, screen_height))

ball = pygame.Rect(screen_width/2, screen_height/2, 30,30)
wall1 = pygame.Rect(screen_width- 40, screen_height/ 2 - 75, 20,150)
wall2 = pygame.Rect(20, screen_height / 2 - 70, 20, 140)
wall1_speed = 0
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)


class Ball:
        def __init__(self, x, y, width , height, speed_x, speed_y, screen_width, screen_height):
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
            if self.rect.left <= 0 or self.rect.right >= self.screen_width:
                 self.speed_x *=-1
            #checking for collision with walls, then bounce back
            if self.rect.colliderect(wall1) or self.rect.colliderect(wall2):
                 self.speed_x *=-1

ball = Ball(300, 200, 20, 20, 15, 15, screen_width, screen_height)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                wall1_speed +=10
            if event.key == pygame.K_UP:
                wall1_speed -=10
            if event.key == pygame.K_UP:
                wall1_speed -=10
            if event.key == pygame.K_DOWN:
                wall1_speed +=10
            
        ball.physics(wall1,wall2)
        wall1.y += wall1_speed
        if wall1.top <= 0:
            wall1.top = 0
        if wall1.bottom >= screen_height:
            wall1.bottom = screen_height


        screen.fill(bg_color)
        pygame.draw.rect(screen,light_grey, wall1)
        pygame.draw.rect(screen,light_grey, wall2)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.line(screen, light_grey, (screen_width/2, 0), (screen_width/ 2, screen_height))
        

        
    
    
    pygame.display.flip()
    clock.tick(144)
