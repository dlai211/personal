import sys, pygame, math
import pygame.gfxdraw
import numpy as np
from bottom_piece import draw_piece_inventory, draw_game_pieces, rotate_point

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# player
BLUE1 = (202, 244, 255)
BLUE2 = (160, 222, 255)
BLUE3 = (90, 178, 255)
# AI
ORANGE1 = (224, 195, 252)
ORANGE2 = (218, 182, 252)
ORANGE3 = (187, 173, 255)

# Proportions & Sizes
WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 2.7
CIRCLE_WIDTH = 8
SQUARE_WIDTH = 5
TRI_WIDTH = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board = [[(0, 0) for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color,
                         (0, SQUARE_SIZE * i),
                         (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color,
                         (SQUARE_SIZE * i, 0),
                         (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_all_game_pieces(screen, game_pieces):
    for pieces in game_pieces:
        row = pieces['position'][0]
        col = pieces['position'][1]
        size = pieces['size']
        player = pieces['player']

        if size == 3 and player == 1:
            x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            radius = int(CIRCLE_RADIUS)  # Convert CIRCLE_RADIUS to an integer
            pygame.gfxdraw.filled_circle(screen, x, y, radius, ORANGE3)
            pygame.gfxdraw.aacircle(screen, x, y, radius, ORANGE3)  # Anti-aliased outline

        if size == 2 and player == 1:
            square_width = CIRCLE_RADIUS / np.sqrt(2) * 0.8  # 0.8 is the square adjustment
            pygame.draw.rect(screen, ORANGE2, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                               int(row * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                               square_width * 2, square_width * 2))

        if size == 1 and player == 1:
            # Parameters for the triangle's center and size
            center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            side_length = CIRCLE_RADIUS / np.sqrt(2) * 0.8 * 2 * 0.78  # Roughly equivalent size to the square

            height = side_length * (np.sqrt(3) / 2)  # Height of an equilateral triangle

            # Vertex coordinates
            v1 = (center_x, center_y - 2 / 3 * height)
            v2 = (center_x - side_length / 2, center_y + 1 / 3 * height)
            v3 = (center_x + side_length / 2, center_y + 1 / 3 * height)

            rv1 = rotate_point((center_x, center_y), v1, 20)
            rv2 = rotate_point((center_x, center_y), v2, 20)
            rv3 = rotate_point((center_x, center_y), v3, 20)

            # Draw the triangle
            pygame.draw.polygon(screen, ORANGE1, [rv1, rv2, rv3])

        if size == 3 and player == 2:
            x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            radius = int(CIRCLE_RADIUS)  # Convert CIRCLE_RADIUS to an integer
            pygame.gfxdraw.filled_circle(screen, x, y, radius, BLUE3)
            pygame.gfxdraw.aacircle(screen, x, y, radius, BLUE3)  # Anti-aliased outline

        if size == 2 and player == 2:
            square_width = CIRCLE_RADIUS / np.sqrt(2) * 0.8  # 0.8 is the square adjustment
            pygame.draw.rect(screen, BLUE2, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                             int(row * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                             square_width * 2, square_width * 2))

        if size == 1 and player == 2:
            # Parameters for the triangle's center and size
            center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            side_length = CIRCLE_RADIUS / np.sqrt(2) * 0.8 * 2 * 0.78  # Roughly equivalent size to the square

            height = side_length * (np.sqrt(3) / 2)  # Height of an equilateral triangle

            # Vertex coordinates
            v1 = (center_x, center_y - 2 / 3 * height)
            v2 = (center_x - side_length / 2, center_y + 1 / 3 * height)
            v3 = (center_x + side_length / 2, center_y + 1 / 3 * height)

            rv1 = rotate_point((center_x, center_y), v1, 20)
            rv2 = rotate_point((center_x, center_y), v2, 20)
            rv3 = rotate_point((center_x, center_y), v3, 20)

            # Draw the triangle
            pygame.draw.polygon(screen, BLUE1, [rv1, rv2, rv3])


def mark_square(row, col, player, size):
    board[row][col] = (player, size)


def is_board_full(check_board=board):
    player1_count = 0
    player2_count = 0

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            player, size = check_board[row][col]
            if player == 0:
                return False
            elif player == 1: # player
                player1_count += 1
            elif player == 2: # ai
                player2_count += 1

    if player2_count > player1_count:
        return float('inf')  # AI wins
    if player1_count > player2_count:
        return float('-inf')  # Player wins
    return 0


def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col][0] == player and check_board[1][col][0] == player and check_board[2][col][0] == player:
            return True

    for row in range(BOARD_ROWS):
        if check_board[row][0][0] == player and check_board[row][1][0] == player and check_board[row][2][0] == player:
            return True

    if check_board[0][0][0] == player and check_board[1][1][0] == player and check_board[2][2][0] == player:
        return True

    if check_board[0][2][0] == player and check_board[1][1][0] == player and check_board[2][0][0] == player:
        return True

    return False

# player_pieces = {'S': 3, 'M': 3, 'L': 2}
# ai_pieces = {'S': 3, 'M': 3, 'L': 2}
player_pieces = [3, 3, 2]
ai_pieces = [3, 3, 2]


def can_place_piece(row, col, size, player, minimax_board, available_pieces):
    '''
    1. Check if ai_game_piece bigger than existing shape
    2. Check if ai_game_piece NOT place on another ai_game_piece (player != 2)
    3. Check if ai_game_piece still available
    '''
    if size > minimax_board[row][col][1] and player != minimax_board[row][col][0] and available_pieces[size-1] != 0:
        return True
    else:
        return False

def place_piece(row, col, size, player, minimax_board, available_pieces):
    minimax_board[row][col] = (player, size)
    available_pieces[size-1] -= 1

def remove_piece(row, col, minimax_board, available_pieces, size, previous_state):
    minimax_board[row][col] = previous_state  # restore previous state if necessary
    available_pieces[size-1] += 1


def minimax(minimax_board, depth, is_maximizing, player_available_pieces=player_pieces, ai_available_pieces=ai_pieces, max_depth=3):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        result = is_board_full(minimax_board)
        if result is False:
            return 0
        else:
            return result
    if depth == max_depth:
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                for size in (1, 2, 3):
                    if can_place_piece(row, col, size, 2, minimax_board, ai_available_pieces):
                        tmp = minimax_board[row][col]
                        place_piece(row, col, size, 2, minimax_board, ai_available_pieces)
                        score = minimax(minimax_board, depth + 1, False, player_available_pieces, ai_available_pieces, max_depth)
                        remove_piece(row, col, minimax_board, ai_available_pieces, size, tmp)
                        best_score = max(best_score, score)
                        print(f"Maximizing: Depth={depth}, Row={row}, Col={col}, Size={size}, Score={score}")
        return best_score

    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                for size in (1, 2, 3):
                    if can_place_piece(row, col, size, 1, minimax_board, player_available_pieces):
                        tmp = minimax_board[row][col]
                        place_piece(row, col, size, 1, minimax_board, player_available_pieces)
                        score = minimax(minimax_board, depth + 1, True, player_available_pieces, ai_available_pieces, max_depth)
                        remove_piece(row, col, minimax_board, player_available_pieces, size, tmp)
                        best_score = min(best_score, score)
                        print(f"Minimizing: Depth={depth}, Row={row}, Col={col}, Size={size}, Score={score}")
        return best_score


def best_move():
    best_score = -1000
    move = (-1, -1, 0)
    board2 = board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            for size in (1, 2, 3):
                if can_place_piece(row, col, size, 2, board2, ai_pieces):
                    tmp = board[row][col]
                    place_piece(row, col, size, 2, board2, ai_pieces)
                    score = minimax(board2, 0, False, player_pieces, ai_pieces)
                    remove_piece(row, col, board2, ai_pieces, size, tmp)
                    if score > best_score:
                        best_score = score
                        move = (row, col, size)

    if move != (-1, -1, 0):
        print(move)
        mark_square(move[0], move[1], 2, move[2])
        ai_pieces[move[2]-1] -= 1
        print(ai_pieces)
        return True, move[0], move[1], move[2]

    return False, move[0], move[1], move[2]

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = (0, 0)

# Initialize game pieces area
# Additional space at the bottom
screen = pygame.display.set_mode((WIDTH, HEIGHT * 7/5))

# New game piece settings
dragging = False
drag_index = None
dragged_piece_index = None
dragged_piece_origin = None
player_game_pieces = [
    (WIDTH * 0.3, HEIGHT + 50, 3),
    (WIDTH * 0.55, HEIGHT + 50, 2),
    (WIDTH * 0.8, HEIGHT + 50, 1)
]
ai_game_pieces = [
    (WIDTH * 0.3, HEIGHT + 150, 3),
    (WIDTH * 0.55, HEIGHT + 150, 2),
    (WIDTH * 0.8, HEIGHT + 150, 1)
]

def check_collision(x, y, game_pieces):
    for idx, (cx, cy, size) in enumerate(game_pieces):
        distance = math.sqrt((cx - x) ** 2 + (cy - y) ** 2)
        if distance < CIRCLE_RADIUS:
            return idx, size
    return None, None

## To-do: piece_exist when it is place on blue's small piece and not myself
def piece_exists(game_pieces, new_piece):
    for piece in game_pieces:
        if (new_piece['size'] > piece['size'] and
            new_piece['player'] != piece['player']):
            return True
    return False


player = 1
game_over = False
dragged_size = 0
game_pieces = [{'size': 0,
                'player': 0,
                'position': (-1, -1)}]

while True:
    screen = pygame.display.set_mode((WIDTH, HEIGHT * 7 / 5))
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            if player == 1:  # Ensure only player can drag their pieces
                drag_index, dragged_size = check_collision(*pos, player_game_pieces)
                if drag_index is not None:
                    dragging = True
                    dragged_piece_index = drag_index
                    dragged_piece_origin = (player_game_pieces[drag_index][0], player_game_pieces[drag_index][1])  # Keep the original click position

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            print(row, col, dragged_size, piece_exists(game_pieces, {'size': dragged_size, 'player': 1, 'position': (row, col)}))
            if col < 3 and row < 3 and piece_exists(game_pieces, {'size': dragged_size, 'player': 1, 'position': (row, col)}): # so it does NOT go out of the map
                if dragged_size == 3 and player_pieces[2] > 0:

                    mark_square(row, col, player, dragged_size)
                    player_pieces[2] -= 1
                    game_pieces.append({'size': 3, 'player': 1, 'position': (row, col)})
                    player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)
                    player = player % 2 + 1
                    if not game_over:
                        BestMove, row, col, size_tmp = best_move()
                        if BestMove:
                            game_pieces.append({'size': size_tmp, 'player': 2, 'position': (row, col)})
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1

                    if not game_over:
                        if is_board_full():
                            game_over = True

                else: player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)

                if dragged_size == 2 and player_pieces[1] > 0:

                    mark_square(row, col, player, dragged_size)
                    player_pieces[1] -= 1
                    game_pieces.append({'size': 2, 'player': 1, 'position': (row, col)})
                    player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)
                    player = player % 2 + 1
                    if not game_over:
                        BestMove, row, col, size_tmp = best_move()
                        if BestMove:
                            game_pieces.append({'size': size_tmp, 'player': 2, 'position': (row, col)})
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1
                    if not game_over:
                        if is_board_full():
                            game_over = True

                else: player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)

                if dragged_size == 1 and player_pieces[0] > 0:

                    mark_square(row, col, player, dragged_size)
                    player_pieces[0] -= 1
                    game_pieces.append({'size': 1, 'player': 1, 'position': (row, col)})
                    player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)
                    player = player % 2 + 1
                    if not game_over:
                        BestMove, row, col, size_tmp = best_move()
                        if BestMove:
                            game_pieces.append({'size': size_tmp, 'player': 2, 'position': (row, col)})

                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1

                    if not game_over:
                        if is_board_full():
                            game_over = True

                else: player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)

            else: # Reset the piece position if it's not a valid drop
                player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)

            dragging = False
            dragged_piece_index = None
            dragged_piece_origin = None

        if event.type == pygame.MOUSEMOTION and dragging:
            # Move piece with mouse
            mouseX, mouseY = pygame.mouse.get_pos()
            player_game_pieces[drag_index] = (mouseX, mouseY, dragged_size)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_lines()
        draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                             [player_pieces[2], player_pieces[1], player_pieces[0],
                              ai_pieces[2], ai_pieces[1], ai_pieces[0]])
        draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2, BLUE2,
                         ORANGE3, BLUE3)
        # draw_figures()
        draw_all_game_pieces(screen, game_pieces)

    else:
        if check_win(1):
            draw_all_game_pieces(screen, game_pieces)
            draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                                 [player_pieces[2], player_pieces[1], player_pieces[0],
                                  ai_pieces[2], ai_pieces[1], ai_pieces[0]])
            draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2,
                             BLUE2, ORANGE3, BLUE3)
            draw_lines(GREEN)
        elif check_win(2):
            draw_all_game_pieces(screen, game_pieces)
            draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                                 [player_pieces[2], player_pieces[1], player_pieces[0],
                                  ai_pieces[2], ai_pieces[1], ai_pieces[0]])
            draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2,
                             BLUE2, ORANGE3, BLUE3)
            draw_lines(RED)
        else:
            draw_all_game_pieces(screen, game_pieces)
            draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                                 [player_pieces[2], player_pieces[1], player_pieces[0],
                                  ai_pieces[2], ai_pieces[1], ai_pieces[0]])
            draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2,
                             BLUE2, ORANGE3, BLUE3)
            if is_board_full(board):
                result = is_board_full(board)
                if result == float('inf'):
                    draw_lines(GREEN)
                if result == float('-inf'):
                    draw_lines(RED)


    pygame.display.update()



