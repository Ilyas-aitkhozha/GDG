import pygame

pygame.init()
size_block = 200
margin = 20
width = height = size_block * 3 + margin * 4
arr = [[0] * 3 for i in range(3)]
next_move = 0
screen = pygame.display.set_mode((width,height))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (size_block + margin)
            row = y_mouse // (size_block + margin)
            if arr[row][col] == 0:
                if next_move % 2 == 0:
                    arr[row][col] = 'x'
                else:
                    arr[row][col] = '0'
                next_move +=1
    for col in range(3):
        for row in range(3):
            if arr[row][col] == 'x':
                color = (255,0,0)
            elif arr[row][col] == '0':
                color = (0,255,0)
            else:
                color = (255,255,255)
            x = col * size_block + (col+1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x,y,size_block,size_block))
            if color == (255,0,0):
                pygame.draw.line(screen, (255,255,255), (x + 5,y + 5), (x+size_block -5 , y+size_block- 5), 10)
                pygame.draw.line(screen, (255,255,255), (x +size_block -5 ,y +  5), (x+5 , y+size_block- 5), 10)
            elif color == (0,255,0):
                pygame.draw.circle(screen, (255,255,255),(x + (size_block // 2) ,y + (size_block//2)), 80, 10)
        pygame.display.update()
