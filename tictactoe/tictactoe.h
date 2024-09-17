#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <string>
#include <limits>
#include <algorithm>
#include <vector>

void draw_gameboard(std::vector<std::vector<int>>& board) {
    std::cout << " " << board[0][0] << " | " << board[1][0] << " | " << board[2][0] << std::endl;
    std::cout << "___|___|___" << std::endl;
    std::cout << " " << board[3][0] << " | " << board[4][0] << " | " << board[5][0] << std::endl;
    std::cout << "___|___|___" << std::endl;
    std::cout << " " << board[6][0] << " | " << board[7][0] << " | " << board[8][0] << std::endl;
    std::cout << "   |   |   " << std::endl;
}

void place_piece(std::vector<std::vector<int>>& board, int index, int role, int size, std::vector<int>& available_pieces) {
    board[index][0] = role;
    // available_pieces[size]--;
}

void remove_piece(std::vector<std::vector<int>>& board, int index, int size, std::vector<int>& available_pieces, std::vector<int>& previous_state) {
    board[index] = previous_state;
    // available_pieces[size]++;
}

bool available_square(std::vector<std::vector<int>> board, int index) {
    return board[index][0] == 0;
}

int is_board_full(std::vector<std::vector<int>> board) {
    for (int i = 0; i < 9; i++) {
        if (board[i][0] == 0) {
            return 0;
        }
    }
    return 1;
}

bool check_win(std::vector<std::vector<int>> board, int role) {
    std::vector<std::vector<int>> winConditions = {
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
        {0, 4, 8}, {2, 4, 6}
    };

    for (const auto& combination : winConditions) {
        if (board[combination[0]][0] == role && board[combination[1]][0] == role && board[combination[2]][0] == role) {
            return true;
        }
    }
    return false;
}


int minimax(std::vector<std::vector<int>>& minimax_board, int depth, bool is_maximizing) {
    
    int posInf = std::numeric_limits<int>::max();
    int negInf = std::numeric_limits<int>::min();
    int best_score, score;


    if (check_win(minimax_board, 2)) {
        return posInf;
    } else if (check_win(minimax_board, 1)) {
        return negInf;
    } else if (is_board_full(minimax_board)) {
        return 0;
    }

    if (is_maximizing) {
        best_score = -1000;
        for (int index = 0; index < 3; index++) {
            if (minimax_board[index][0] == 0) {
                minimax_board[index][0] = 2;
                score = minimax(minimax_board, depth+1, false);
                minimax_board[index][0] = 0;
                best_score = std::max(best_score, score);
            }
        }
        return best_score;
    } else {
        best_score = 1000;
        for (int index = 0; index < 3; index++) {
            if (minimax_board[index][0] == 0) {
                minimax_board[index][0] = 1;
                score = minimax(minimax_board, depth+1, true);
                minimax_board[index][0] = 0;
                best_score = std::min(best_score, score);
            }
        }
        return best_score;
    }
}

int best_move (std::vector<std::vector<int>>& board) {
    int best_score = -1000;
    int score;
    std::vector<int> move = {-1, -1};

    for (int index = 0; index < 3; index++) {
        if (board[index][0] == 0) {
            board[index][0] = 2;
            score = minimax(board, 0, false);
            board[index][0] = 0;
            if (score > best_score) {
                best_score = score;
                move = {index, 0};;
            }
        }
    }

    if (move != std::vector<int>{-1, -1}) {
        place_piece(board, move.at(0), 2);
        return 1;
    }

    return 0;

}


void restart_game(std::vector<std::vector<int>> board) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            board[i][j] = 0;
        }
    }
}


#endif
