import pygame
from sql_data import user_exist, current_data, insert_user_data,update_score,insert_game
#taking input from users 
user_name_x = input("enter user name for X ").strip()
user_name_0 = input("enter user name for 0 ").strip()

#with queries from sqldata checking for existence, and if they didnt play creating new players
if user_exist(user_name_x, user_name_0):
    score_x = current_data(user_name_x)
    score_0 = current_data(user_name_0)
    print(f"welcome, {user_name_x}! continie with score {score_x}")
    print(f"welcome, {user_name_0}! continue with score {score_0}")
else:
    insert_user_data(user_name_x)
    insert_user_data(user_name_0)               
    print("new players")
pygame.init()
size_block = 200
margin = 20
width = height = size_block * 3 + margin * 4
arr = [[0] * 3 for i in range(3)]
next_move = 0
screen = pygame.display.set_mode((width,height))
running = True
game_over = False
# checking, who is winner 
def winner(arr, sign):
    piece_count = 0 
    #if signs is in the row
    for row in arr:
        piece_count +=row.count(0)
        if row.count(sign) == 3:
            return sign
    #if signs is in the column
    for col in range(3):
        if arr[0][col] == sign and arr[1][col] == sign and arr[2][col] == sign:
            return sign
    #checking main diagonal
    if arr[0][0] == sign and arr[1][1] == sign and arr[2][2] == sign:
        return sign
    #checking second diagonal
    if arr[0][2] == sign and arr[1][1] == sign and arr[2][0] == sign:
        return sign
    #if there is zero piece avalaible and no one won, then draw
    if piece_count == 0:
        return "Draw"
    return False
#just drawing the grid (from the youtube channel egorrof_chanel "как создать игровое поле для своей игры в pygame")
def draw_grid():
    for col in range(3):
        for row in range(3):
            #determining whether its x, and if its x using red colors and for 0 green, for avalaible spots white 
            if arr[row][col] == 'x':
                color = (255, 0, 0)
            elif arr[row][col] == '0':
                color = (0, 255, 0)
            else:
                color = (255, 255, 255)
            #formula for placing boxes next to each other
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, size_block, size_block))
            #drawing x
            if color == (255, 0, 0):
                pygame.draw.line(screen, (255, 255, 255), (x + 5, y + 5), (x + size_block - 5, y + size_block - 5), 10)
                pygame.draw.line(screen, (255, 255, 255), (x + size_block - 5, y + 5), (x + 5, y + size_block - 5), 10)
            #drawing circle
            elif color == (0, 255, 0):
                pygame.draw.circle(screen, (255, 255, 255), (x + (size_block // 2), y + (size_block // 2)), size_block // 2, 10)
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        # if we are clicking, and game isnt over then: get position of the mouse.
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (size_block + margin)
            row = y_mouse // (size_block + margin)
            # and here we are checking, if spot is avalaible, then checking order, if its even, then x, odd = 0
            if arr[row][col] == 0:
                if next_move % 2 == 0:
                    arr[row][col] = 'x'
                else:
                    arr[row][col] = '0'
                next_move +=1
        #for next game, press space, and then grid will draw automatically, with start values
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_over = False
            arr = [[0] * 3 for i in range(3)]
            next_move = 0
            screen.fill((0, 0, 0))
            draw_grid()

    # checking, if someone won or not
    if not game_over:
        result_x = winner(arr, 'x')
        result_0 = winner(arr, '0')
        if result_x == 'x':
            #updating results if x won
            update_score(user_name_x)
            insert_game(user_name_x, user_name_0, 'x')
            game_over = 'x'
        elif result_0 == '0':
            #the same thing
            update_score(user_name_0)
            insert_game(user_name_x, user_name_0, '0')
            game_over = '0'
        elif result_x == 'Draw':
            insert_game(user_name_x, user_name_0, 'draw')
            game_over = 'Draw'
    draw_grid()
    # if game is over, fill screen with black, and print who won
    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('stxingkai', 80)
        text1 = font.render(game_over, True, (255, 255, 255))
        text_rect = text1.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text1, [text_x, text_y])
    pygame.display.update()
