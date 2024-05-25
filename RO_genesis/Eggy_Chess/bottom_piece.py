import pygame, math
import numpy as np

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT * 7/5))


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


    # # AI pieces
    # x_offset = 10
    # label2 = font.render(f'AI:', True, BLUE1)
    # screen.blit(label2, (x_offset, y_offset+100))
    # x_offset += label1.get_width() + 85
    #
    # for i in range(3, 6):
    #
    #     label = font.render(f'x{NUM[i]}', True, BLUE1)
    #     screen.blit(label, (x_offset, y_offset+100))
    #     x_offset += label.get_width() + 85

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
