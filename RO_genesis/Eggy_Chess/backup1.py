import sys, pygame, math
import numpy as np
from pyglet import event

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
ORANGE1 = (255, 242, 215)
ORANGE2 = (248, 199, 148)
ORANGE3 = (216, 174, 126)

# Proportions & Sizes
WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 8
SQUARE_WIDTH = 5
TRI_WIDTH = 4
CROSS_WIDTH = 18

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Function to calculate the rotation of points
def rotate_point(center, point, angle):
    angle_rad = math.radians(angle)
    return (
        center[0] + math.cos(angle_rad) * (point[0] - center[0]) - math.sin(angle_rad) * (point[1] - center[1]),
        center[1] + math.sin(angle_rad) * (point[0] - center[0]) + math.cos(angle_rad) * (point[1] - center[1])
    )

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color,
                         (0, SQUARE_SIZE * i),
                         (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color,
                         (SQUARE_SIZE * i, 0),
                         (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)


def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1: # player
                pygame.draw.circle(screen, ORANGE3, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                   int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
                square_width = CIRCLE_RADIUS / np.sqrt(2) * 0.8 # 0.8 is the square adjustment
                pygame.draw.rect(screen, ORANGE2, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                                 int(row * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                                 square_width*2, square_width*2), SQUARE_WIDTH)

                # Parameters for the triangle's center and size
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
                center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
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
                pygame.draw.polygon(screen, ORANGE1, [rv1, rv2, rv3], TRI_WIDTH)

            elif board[row][col] == 2: # AI
                pygame.draw.circle(screen, BLUE3, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                   int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
                square_width = CIRCLE_RADIUS / np.sqrt(2) * 0.8 # 0.8 is the square adjustment
                pygame.draw.rect(screen, BLUE2, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                                 int(row * SQUARE_SIZE + SQUARE_SIZE // 2 - square_width),
                                                 square_width*2, square_width*2), SQUARE_WIDTH)

                # Parameters for the triangle's center and size
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
                center_y = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
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
                pygame.draw.polygon(screen, BLUE1, [rv1, rv2, rv3], TRI_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(best_score, score)
        return best_score


def best_move():
    best_score = -1000
    move = (-1, 1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, 1):
        mark_square(move[0], move[1], 2)
        return True

    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True

                player = player % 2 + 1  # alternating the player

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()

    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)


    pygame.display.update()







































