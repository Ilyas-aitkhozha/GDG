import pygame
import random

BOARD_SIZE = 10           # размер поле
CELL_SIZE = 40         
MARGIN = 5               
SCREEN_WIDTH = 2 * (BOARD_SIZE * (CELL_SIZE + MARGIN)) + 100  # две доски с промежутком
SCREEN_HEIGHT = BOARD_SIZE * (CELL_SIZE + MARGIN) + 150

COLOR_BG = (30, 30, 30)
COLOR_WATER = (0, 100, 200)
COLOR_SHIP = (50, 50, 50)
COLOR_HIT = (200, 0, 0)
COLOR_MISS = (220, 220, 220)
COLOR_GRID = (0, 0, 0)
COLOR_TEXT = (255, 255, 255)

def can_place(board, row, col, length, orientation):
    rows = len(board)
    cols = len(board[0])
    if orientation == 'H':
        if col + length > cols: return False
        r0, r1 = row-1, row+1 #снизу сверху
        c0, c1 = col-1, col+length #слева до конца корабля
    else:
        if row + length > rows: return False
        r0, r1 = row-1, row+length #снизу до конца сверху
        c0, c1 = col-1, col+1 #слева справа
    for rr in range(r0, r1+1):
        for cc in range(c0, c1 + 1):
            if 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] != 0:
                return False
    return True

def place_ship(board, ship_id, length):
    """Рандомно размещает корабль с уникальным айдишкой  с заданной длины."""
    rows = len(board)
    cols = len(board[0])
    placed = False
    while not placed:
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - length)
        else:
            row = random.randint(0, rows - length)
            col = random.randint(0, cols - 1)
        
        if can_place(board, row, col, length, orientation):
            if orientation == 'H':
                for i in range(length):
                    board[row][col + i] = ship_id
            else:
                for i in range(length):
                    board[row + i][col] = ship_id
            placed = True

def generate_board(ships, board_size=10):
    board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    current_ship_id = 1
    for ship_length, count in ships:
        for _ in range(count):
            place_ship(board, current_ship_id, ship_length)
            current_ship_id += 1
    return board


enemy_targets = []


def enemy_shot(player_board, shots_made):
    """
    Enemy выбирает случайную ячейку на поле игрока, куда еще не стрелял Обновляет поле: если клетка пуста отмечает промахом (-99),
    если в клетке корабль  меняет значение на отрицательное
    """
    rows = len(player_board)
    cols = len(player_board[0])
    available = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in shots_made]
    if not available:
        return None
    if enemy_targets:
        for _ in range(len(enemy_targets)):
            r, c = enemy_targets.pop(0)
            if (r, c) in available:
                row, col = r, c
                break
        else:
            enemy_targets.clear()
            row, col = random.choice(available)
    else:
        row, col = random.choice(available)

    shots_made.add((row, col))
    cell = player_board[row][col]
    if cell == 0:
        player_board[row][col] = -99
        return (row, col, "Промах", None)

    if cell < 0:
        return (row, col, "Уже стреляли", None)

    # попадание — помечаем и добавляем соседей в очередь
    ship_id = cell
    player_board[row][col] = -ship_id
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = row+dr, col+dc
        if (nr, nc) in available and (nr, nc) not in enemy_targets:
            enemy_targets.append((nr, nc))

    # проверяем, потонул ли корабль
    alive = any(player_board[r][c] == ship_id for r in range(rows) for c in range(cols))
    if not alive:
        enemy_targets.clear()
        return (row, col, "Уничтожен корабль", ship_id)

    return (row, col, "Попадание", None)


    

def player_shot(enemy_board, shots_made, row, col):
    """
    Обрабатывает выстрел игрока по полю enemy. Если клетка уже выбрана, возвращает что чел уже стрелял.
    Если промах, отмечает -99, если попадание изменяет значение на отрицательное.
    """
    rows = len(enemy_board)
    cols = len(enemy_board[0])
    if (row, col) in shots_made:
        return (row, col, "Уже стрелял", None)
    shots_made.add((row, col))
    
    cell = enemy_board[row][col]
    if cell == 0:
        enemy_board[row][col] = -99  # промах
        return (row, col, "Промах", None)
    else:
        if cell < 0:
            return (row, col, "Уже стрелял", None)
        ship_id = cell
        enemy_board[row][col] = -ship_id  # попадание
        still_alive = any(enemy_board[r][c] == ship_id for r in range(rows) for c in range(cols))
        if still_alive:
            return (row, col, "Попадание", None)
        else:
            return (row, col, "Уничтожен корабль", ship_id)

def draw_board(surface, board, top_left, hide_ships=False):
    font = pygame.font.SysFont(None, 24)
    x0, y0 = top_left
    for r in range(len(board)):
        for c in range(len(board[0])):
            cell = board[r][c]
            rect = pygame.Rect(x0 + c * (CELL_SIZE + MARGIN),
                               y0 + r * (CELL_SIZE + MARGIN),
                               CELL_SIZE, CELL_SIZE)
            
            if cell == 0:
                color = COLOR_WATER
            elif cell == -99:
                color = COLOR_MISS
            elif cell < 0:
                color = COLOR_HIT
            else:
                color = COLOR_SHIP if not hide_ships else COLOR_WATER

            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, COLOR_GRID, rect, 1)
            
            if cell > 0 and not hide_ships:
                text = font.render(str(cell), True, COLOR_TEXT)
                surface.blit(text, (rect.x + 5, rect.y + 5))
def win_or_lose(player_board, enemy_board):
    """
    Проверяет, выиграл ли игрок или проиграл.
    Возвращает 'win', 'lose' или None.
    """
    enemy_alive = any(cell > 0 for row in enemy_board for cell in row)
    player_alive = any(cell > 0 for row in player_board for cell in row)

    if not enemy_alive:
        return 'win'
    elif not player_alive:
        return 'lose'
    else:
        return None
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Морской бой на PyGame")
    clock = pygame.time.Clock()

    # 4 одиночных (1-клеточные), 3 двуклеточных (2-клеточные), 2 трёхклеточных (3-клеточные)
    ships = [
        (1, 4),
        (2, 3),
        (3, 2)
    ]
    
    player_board = generate_board(ships, board_size=BOARD_SIZE)
    enemy_board = generate_board(ships, board_size=BOARD_SIZE)
    
    enemy_shots = set()   # координаты куда enemy уже стрелял по player_board
    player_shots = set()  # координаты, куда игрок уже стрелял по enemy_board

    player_top_left = (50, 50)
    enemy_top_left = (SCREEN_WIDTH // 2 + 20, 50)

    running = True
    message = ""
    font_msg = pygame.font.SysFont(None, 28)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                # Проверяем, попал ли клик в чела(врага)
                ex, ey = enemy_top_left
                board_width = BOARD_SIZE * (CELL_SIZE + MARGIN) - MARGIN
                board_height = BOARD_SIZE * (CELL_SIZE + MARGIN) - MARGIN
                #проверяем на все условие ex= enemy x
                if ex <= mx <= ex + board_width and ey <= my <= ey + board_height:
                    col = (mx - ex) // (CELL_SIZE + MARGIN)
                    row = (my - ey) // (CELL_SIZE + MARGIN)
                    shot = player_shot(enemy_board, player_shots, row, col)
                    if shot:
                        r, c, result, drop_ship = shot
                        message = f"Player: ({r}, {c}) - {result}"
                        if drop_ship is not None:
                            message += f" (Корабль {drop_ship} уничтожен)"
                        
                        # После выстрела игрока запускаем выстрел enemy по полю игрока
                        enemy_result = enemy_shot(player_board, enemy_shots)
                        if enemy_result:
                            er, ec, eresult, esunk = enemy_result
                            message += f" | Enemy: ({er}, {ec}) - {eresult}"
                            if esunk is not None:
                                message += f" (Корабль {esunk} уничтожен)"
                        else:
                            message += " | Enemy: Нет доступных ячеек для выстрелов."
                        
                        result = win_or_lose(player_board, enemy_board)
                        if result:
                            end_font = pygame.font.SysFont(None, 40)
                            if result == 'win':
                                end_text = "Победа! все его корабли разрушены."
                            else:
                                end_text = "Поражение! Все твои корабли уничтожены."
                            surf = end_font.render(end_text, True, COLOR_TEXT)
                            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                            screen.fill(COLOR_BG)
                            screen.blit(surf, rect)
                            pygame.display.flip()
                            pygame.time.delay(3000)
                            running = False
        
        screen.fill(COLOR_BG)
        
        title_font = pygame.font.SysFont(None, 32)
        player_text = title_font.render("Поле игрока", True, COLOR_TEXT)
        enemy_text = title_font.render("Поле enemy", True, COLOR_TEXT)
        screen.blit(player_text, (player_top_left[0], player_top_left[1] - 30))
        screen.blit(enemy_text, (enemy_top_left[0], enemy_top_left[1] - 30))
        
        draw_board(screen, player_board, player_top_left, hide_ships=False)
        draw_board(screen, enemy_board, enemy_top_left, hide_ships=True)
        
        # ыывод сообщения о результате выстрелов
        msg_surface = font_msg.render(message, True, COLOR_TEXT)
        screen.blit(msg_surface, (50, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(15)
    
    pygame.quit()

if __name__ == '__main__':
    main()
