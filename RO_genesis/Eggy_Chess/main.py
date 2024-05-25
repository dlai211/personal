import sys, pygame, math, time
import pygame.gfxdraw
import numpy as np
# from bottom_piece import draw_piece_inventory, draw_game_pieces, rotate_point

# Initialization code and constants
pygame.init()

# Colors and other constants
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
# AI
BLUE1 = (202, 244, 255)
BLUE2 = (160, 222, 255)
BLUE3 = (90, 178, 255)
# Player
ORANGE1 = (224, 195, 252)
ORANGE2 = (218, 182, 252)
ORANGE3 = (187, 173, 255)

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

def draw_selection_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)

    # Draw Player Button
    player_text = font.render('Player', True, WHITE)
    player_rect = player_text.get_rect(center=(WIDTH // 4, HEIGHT // 2))
    pygame.draw.rect(screen, ORANGE2, player_rect.inflate(20, 20))
    screen.blit(player_text, player_rect)

    # Draw AI Button
    ai_text = font.render('AI', True, WHITE)
    ai_rect = ai_text.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))
    pygame.draw.rect(screen, BLUE2, ai_rect.inflate(20, 20))
    screen.blit(ai_text, ai_rect)

    pygame.display.flip()
    return player_rect, ai_rect


def handle_selection_click(player_rect, ai_rect):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if player_rect.collidepoint(pos):
                return 1  # Player goes first
            if ai_rect.collidepoint(pos):
                return 2  # AI goes first
    return None

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color,
                         (0, SQUARE_SIZE * i),
                         (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color,
                         (SQUARE_SIZE * i, 0),
                         (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1, NUM):
    # Draw the player's inventory
    x_offset = 10
    y_offset = HEIGHT + 50
    font = pygame.font.Font(None, 40)

    # Player pieces
    label1 = font.render(f'Player:', True, ORANGE1)
    screen.blit(label1, (x_offset, y_offset))
    x_offset += label1.get_width() + 85

    for i in range(3):

        label = font.render(f'x{NUM[i]}', True, ORANGE1)
        screen.blit(label, (x_offset, y_offset))
        x_offset += label.get_width() + 85


    # AI pieces
    x_offset = 10
    label2 = font.render(f'AI:', True, BLUE1)
    screen.blit(label2, (x_offset, y_offset+100))
    x_offset += label1.get_width() + 85

    for i in range(3, 6):

        label = font.render(f'x{NUM[i]}', True, BLUE1)
        screen.blit(label, (x_offset, y_offset+100))
        x_offset += label.get_width() + 85

def rotate_point(center, point, angle): # Function to calculate the rotation of points
    angle_rad = math.radians(angle)
    return (
        center[0] + math.cos(angle_rad) * (point[0] - center[0]) - math.sin(angle_rad) * (point[1] - center[1]),
        center[1] + math.sin(angle_rad) * (point[0] - center[0]) + math.cos(angle_rad) * (point[1] - center[1])
    )

def draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2, BLUE2, ORANGE3, BLUE3):
    # Player
    circle_radius_tmp = CIRCLE_RADIUS*2/3
    pygame.draw.circle(screen, ORANGE3, (player_game_pieces[0][0], player_game_pieces[0][1]), circle_radius_tmp)  # Remove the width argument to fill the circle

    square_width = circle_radius_tmp / np.sqrt(2) * 0.8  # 0.8 is the square adjustment
    pygame.draw.rect(screen, ORANGE2, (int(player_game_pieces[1][0] - square_width),
                                       int(player_game_pieces[1][1] - square_width),
                                       square_width * 2, square_width * 2))  # Remove the width argument to fill the square

    # Parameters for the triangle's center and size
    center_x = player_game_pieces[2][0]
    center_y = player_game_pieces[2][1]
    side_length = square_width * 2 * 0.78  # Roughly equivalent size to the square

    height = side_length * (np.sqrt(3) / 2)  # Height of an equilateral triangle

    # Vertex coordinates
    v1 = (center_x, center_y - 2 / 3 * height)
    v2 = (center_x - side_length / 2, center_y + 1 / 3 * height)
    v3 = (center_x + side_length / 2, center_y + 1 / 3 * height)

    rv1 = rotate_point((center_x, center_y), v1, 20)
    rv2 = rotate_point((center_x, center_y), v2, 20)
    rv3 = rotate_point((center_x, center_y), v3, 20)

    # Draw the triangle
    pygame.draw.polygon(screen, ORANGE1, [rv1, rv2, rv3])  # Remove the width argument to fill the triangle

    # AI
    circle_radius_tmp = CIRCLE_RADIUS*2/3
    pygame.draw.circle(screen, BLUE3, (ai_game_pieces[0][0], ai_game_pieces[0][1]), circle_radius_tmp)  # Remove the width argument to fill the circle

    square_width = circle_radius_tmp / np.sqrt(2) * 0.8  # 0.8 is the square adjustment
    pygame.draw.rect(screen, BLUE2, (int(ai_game_pieces[1][0] - square_width),
                                       int(ai_game_pieces[1][1] - square_width),
                                       square_width * 2, square_width * 2))  # Remove the width argument to fill the square

    # Parameters for the triangle's center and size
    center_x = ai_game_pieces[2][0]
    center_y = ai_game_pieces[2][1]
    side_length = square_width * 2 * 0.78  # Roughly equivalent size to the square

    height = side_length * (np.sqrt(3) / 2)  # Height of an equilateral triangle

    # Vertex coordinates
    v1 = (center_x, center_y - 2 / 3 * height)
    v2 = (center_x - side_length / 2, center_y + 1 / 3 * height)
    v3 = (center_x + side_length / 2, center_y + 1 / 3 * height)

    rv1 = rotate_point((center_x, center_y), v1, 20)
    rv2 = rotate_point((center_x, center_y), v2, 20)
    rv3 = rotate_point((center_x, center_y), v3, 20)

    # Draw the triangle
    pygame.draw.polygon(screen, BLUE1, [rv1, rv2, rv3])  # Remove the width argument to fill the triangle

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
    # Check rows
    for row in range(BOARD_ROWS):
        if all(cell[0] == player for cell in check_board[row]):
            return True

    # Check columns
    for col in range(BOARD_COLS):
        if all(check_board[row][col][0] == player for row in range(BOARD_ROWS)):
            return True

    # Check diagonals
    if all(check_board[i][i][0] == player for i in range(BOARD_ROWS)):
        return True
    if all(check_board[i][BOARD_COLS - 1 - i][0] == player for i in range(BOARD_ROWS)):
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


def minimax(minimax_board, depth, alpha, beta, is_maximizing, player_available_pieces, ai_available_pieces, max_depth=5):
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
        return heuristic_evaluation(minimax_board)

    if is_maximizing:
        best_score = -float('inf')
        moves = generate_possible_moves(minimax_board, 2, ai_available_pieces)
        for move in moves:
            row, col, size = move
            tmp = minimax_board[row][col]
            place_piece(row, col, size, 2, minimax_board, ai_available_pieces)
            score = minimax(minimax_board, depth + 1, alpha, beta, False, player_available_pieces, ai_available_pieces, max_depth)
            remove_piece(row, col, minimax_board, ai_available_pieces, size, tmp)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Beta cutoff
        return best_score
    else:
        best_score = float('inf')
        moves = generate_possible_moves(minimax_board, 1, player_available_pieces)
        for move in moves:
            row, col, size = move
            tmp = minimax_board[row][col]
            place_piece(row, col, size, 1, minimax_board, player_available_pieces)
            score = minimax(minimax_board, depth + 1, alpha, beta, True, player_available_pieces, ai_available_pieces, max_depth)
            remove_piece(row, col, minimax_board, player_available_pieces, size, tmp)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Alpha cutoff
        return best_score

def generate_possible_moves(board, player, available_pieces):
    moves = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            for size in (1, 2, 3):
                if can_place_piece(row, col, size, player, board, available_pieces):
                    moves.append((row, col, size))
    return moves

def heuristic_evaluation(board):
    player_score = 0
    ai_score = 0
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            player, size = board[row][col]
            if player == 1:
                player_score += size
            elif player == 2:
                ai_score += size
    return ai_score - player_score


def best_move():
    best_score = -float('inf')
    move = (-1, -1, 0)
    board2 = board
    moves = generate_possible_moves(board2, 2, ai_pieces)
    for row, col, size in moves:
        start_time = time.time()
        tmp = board[row][col]
        place_piece(row, col, size, 2, board2, ai_pieces)
        score = minimax(board2, 0, -float('inf'), float('inf'), False, player_pieces, ai_pieces, max_depth=5)
        remove_piece(row, col, board2, ai_pieces, size, tmp)
        end_time = time.time()
        print(f"Evaluating move -> Row: {row}, Col: {col}, Size: {size}, Score: {score}, Time: {end_time - start_time:.2f} s")
        if score > best_score:
            best_score = score
            move = (row, col, size)

    if move != (-1, -1, 0):
        print(f"Best move found -> Row: {move[0]}, Col: {move[1]}, Size: {move[2]}, Score: {best_score}")
        mark_square(move[0], move[1], 2, move[2])
        ai_pieces[move[2]-1] -= 1
        print(f"AI pieces after move: {ai_pieces}")
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
draw_lines()
draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                     [player_pieces[2], player_pieces[1], player_pieces[0],
                      ai_pieces[2], ai_pieces[1], ai_pieces[0]])
draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2, BLUE2,
                 ORANGE3, BLUE3)
draw_all_game_pieces(screen, game_pieces)

# Show selection menu and get the first player
player_rect, ai_rect = draw_selection_menu()
first_player = None

while first_player is None:
    first_player = handle_selection_click(player_rect, ai_rect)

# Set initial player based on selection
player = first_player

# Handle first move if AI goes first
if player == 2:
    BestMove, row, col, size_tmp = best_move()
    if BestMove:
        game_pieces.append({'size': size_tmp, 'player': 2, 'position': (row, col)})
        if check_win(2):
            game_over = True
            print("AI wins")
        player = player % 2 + 1

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
                    print(f"Piece picked up -> Index: {drag_index}, Size: {dragged_size}")

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            print(f"Piece dropped -> Row: {row}, Col: {col}, Size: {dragged_size}")
            if col < 3 and row < 3 and can_place_piece(row, col, dragged_size, 1, board, player_pieces):  # Ensure valid placement
                mark_square(row, col, player, dragged_size)
                player_pieces[dragged_size - 1] -= 1
                game_pieces.append({'size': dragged_size, 'player': 1, 'position': (row, col)})
                player_game_pieces[dragged_piece_index] = (dragged_piece_origin[0], dragged_piece_origin[1], dragged_size)
                print(f"Piece placed by player -> Row: {row}, Col: {col}, Size: {dragged_size}")

                if check_win(1):
                    game_over = True
                    print("Player wins")
                else:
                    player = player % 2 + 1
                    BestMove, row, col, size_tmp = best_move()
                    if BestMove:
                        game_pieces.append({'size': size_tmp, 'player': 2, 'position': (row, col)})
                        print(f"Piece placed by AI -> Row: {row}, Col: {col}, Size: {size_tmp}")
                        if check_win(2):
                            game_over = True
                            print("AI wins")
                        player = player % 2 + 1

                    if not game_over and is_board_full():
                        game_over = True
                        print("Board is full")

            else:
                # Reset the piece position if it's not a valid drop
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
                print("Game restarted")

    if not game_over:
        draw_lines()
        draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                             [player_pieces[2], player_pieces[1], player_pieces[0],
                              ai_pieces[2], ai_pieces[1], ai_pieces[0]])
        draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2, BLUE2,
                         ORANGE3, BLUE3)
        draw_all_game_pieces(screen, game_pieces)

    else:
        if check_win(1):
            print("Player wins")
            draw_all_game_pieces(screen, game_pieces)
            draw_piece_inventory(screen, HEIGHT, ORANGE1, BLUE1,
                                 [player_pieces[2], player_pieces[1], player_pieces[0],
                                  ai_pieces[2], ai_pieces[1], ai_pieces[0]])
            draw_game_pieces(player_game_pieces, ai_game_pieces, rotate_point, CIRCLE_RADIUS, ORANGE1, BLUE1, ORANGE2,
                             BLUE2, ORANGE3, BLUE3)
            draw_lines(GREEN)
        elif check_win(2):
            print("AI wins")
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





