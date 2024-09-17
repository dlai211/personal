#include "tictactoe.h"


int main() {
        std::vector<std::vector<int>> board = {
            {0, 0}, {0, 0}, {0, 0},
            {0, 0}, {0, 0}, {0, 0},
            {0, 0}, {0, 0}, {0, 0}
        };

        const int player = 1;
        const int ai = 2;
        int currentPlayer = player; 

        int index = -1;
        int winner = -1;


        for (int i = 0; i < 9; i++) {

            //print game board
            draw_gameboard(board);

            if (winner != -1) {
                break;
            }


            std::cout << "You are Player" << currentPlayer << " What is your move? (Type in index 0-9)" << " ";
            while (true) {

                std::cin >> index;


                if (index < 0 || index > 9) {
                    std::cout << "Invalid input, try again." << std::endl;
                }
                else if (board[index][0] != 0) {
                    std::cout << "Tile is full, try again." << std::endl;
                }
                else {
                    break;
                }
                //reset values
                index = -1;
                std::cin.clear(); //clear error flags
                std::cin.ignore(10000, '\n'); //discard values
                //(skips to the next new line \n up to 10000 char) already in input stream
            }

            mark_square(board, index, currentPlayer);
            

            //check winners
            // std::cout << check_win(board, currentPlayer) << std::endl;
            if (check_win(board, currentPlayer)) {
                winner = currentPlayer;
                break;
            } 
            currentPlayer = (currentPlayer == player) ? ai : player;
            
            if (winner == -1) {
                if (best_move(board)) {
                    if (check_win(board, ai)){
                        winner = ai;
                        break;
                    }
                    currentPlayer = (currentPlayer == player) ? ai : player;

                }
            }

        }
        

        if (winner != -1) {
            draw_gameboard(board);
            std::cout << "Player" << winner << " is the winner!" << std::endl;
        } else {
            draw_gameboard(board);
            std::cout << "Tie!" << std::endl;
        }

    }