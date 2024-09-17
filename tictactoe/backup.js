const fs = require('fs'); // Import the file system module (fs)


let board = ["", "", "", "", "", "", "", "", ""];
const humanPlayer = "X";
const aiPlayer = "O";
// let winner = "";
let jsonData = {};

const winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];


function save_move(moveNumber, board, bestMove, winner) {
    let moveKey = `${moveNumber}_move`;

    // If this is the first move of that type, initialize an array
    if (!jsonData[moveKey]) {
        jsonData[moveKey] = [];
    }

    // Add the current move
    jsonData[moveKey].push({
        "board": [...board],
        "bestMove": bestMove,
        "winner": winner
    });
}

function Move(index, check_board, num_move) {
    if (check_board[index] === "") {
        check_board[index] = humanPlayer;

        if (checkWin(check_board, humanPlayer)) {
            save_move(num_move, check_board, null, humanPlayer);
            return;
        }
        let bestMove = aiMove(check_board);
        let board2 = JSON.parse(JSON.stringify(check_board));
        board2[bestMove] = aiPlayer;

        if (checkWin(board2, aiPlayer)) {
            save_move(num_move, check_board, bestMove, aiPlayer);
            return;
        }
        save_move(num_move, check_board, bestMove, "");
    }
}

function aiCheckWin(check_board, bestMove, aiPlayer) {
    check_board[bestMove] = aiPlayer;

    if (checkWin(check_board, aiPlayer)) {
        return true;
    } else {
        return false; }
}

// First player move
for (let index = 0; index < 9; index++) {
    Move(index, board, 1);

    board = restartGame();
}

for (let numMove = 1; numMove < 5; numMove++) {
    if (jsonData[`${numMove}_move`]) {
        for (const move of jsonData[`${numMove}_move`]) {
            if (move.winner === "") {
                // set ai move to board (from previous step)    
                let board2 = [...move.board];
                board2[move.bestMove] = aiPlayer;
                let board3 = JSON.parse(JSON.stringify(board2));

                for (let index2 = 0; index2 < 9; index2++) {
                    Move(index2, board2, numMove+1);
                    board2 = JSON.parse(JSON.stringify(board3));
                    console.log(board2);
                }
            }
        } 
    }
}

// if (jsonData[`${1}_move`]) {
//     jsonData[`${1}_move`].forEach((move) => {

//         if (move.winner === "") {
//             // set ai move to board (from previous step)    
//             let board2 = [...move.board];
//             board2[move.bestMove] = aiPlayer;

//             for (let index2 = 0; index2 < 9; index2++) {
//                 Move(index2, board2, 2);
//                 board2 = move.board;
//                 console.log(board2);
//             }
//         }
//     })
// }



// AI move using Minimax algorithm
function aiMove(board) {
    const bestMove = minimax(board, aiPlayer).index;
    // board[bestMove] = aiPlayer;
    return bestMove;
}

// Check if a player has won
function checkWin(board, player) {
    return winningCombinations.some(combo => {
        return combo.every(index => board[index] === player);
    });
}

function restartGame() {
    return board = ["", "", "", "", "", "", "", "", ""];
}

// Minimax Algorithm
function minimax(newBoard, player) {
    const availableSpots = newBoard.reduce((acc, val, idx) => {
        if (val === "") acc.push(idx);
        return acc;
    }, []);

    // Base cases: terminal states
    if (checkWin(newBoard, humanPlayer)) {
        return { score: -10 };
    } else if (checkWin(newBoard, aiPlayer)) {
        return { score: 10 };
    } else if (availableSpots.length === 0) {
        return { score: 0 };
    }

    // Recursive case: explore all possible moves
    const moves = [];
    for (let i = 0; i < availableSpots.length; i++) {
        const move = {};
        move.index = availableSpots[i];
        newBoard[availableSpots[i]] = player;

        if (player === aiPlayer) {
            const result = minimax(newBoard, humanPlayer);
            move.score = result.score;
        } else {
            const result = minimax(newBoard, aiPlayer);
            move.score = result.score;
        }

        newBoard[availableSpots[i]] = "";
        moves.push(move);
    }

    // Find the best move
    let bestMove;
    if (player === aiPlayer) {
        let bestScore = -Infinity;
        for (let i = 0; i < moves.length; i++) {
            if (moves[i].score > bestScore) {
                bestScore = moves[i].score;
                bestMove = i;
            }
        }
    } else {
        let bestScore = Infinity;
        for (let i = 0; i < moves.length; i++) {
            if (moves[i].score < bestScore) {
                bestScore = moves[i].score;
                bestMove = i;
            }
        }
    }

    return moves[bestMove];
}


fs.writeFileSync('player_first.json', JSON.stringify(jsonData, null, 2), 'utf-8');

console.log('Data has been saved to player_first.json');