const X_CLASS = 'x'
const CIRCLE_CLASS = 'circle'

const SIZE0_CLASS = 'size0';
const SIZE1_CLASS = 'size1';
const SIZE2_CLASS = 'size2';

const WINNING_COMBINATIONS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
]
const cellElements = document.querySelectorAll('[data-cell]')
const board = document.getElementById('board')
const winningMessageElement = document.getElementById('winningMessage')
const restartButton = document.getElementById('restartButton')
const winningMessageTextElement = document.querySelector('[data-winning-message-text]')
let circleTurn

startGame()

restartButton.addEventListener('click', startGame)

function startGame() {
  circleTurn = false
  cellElements.forEach(cell => {
    cell.classList.remove(X_CLASS)
    cell.classList.remove(CIRCLE_CLASS)
    cell.removeEventListener('click', handleClick)
    cell.addEventListener('click', handleClick, { once: true })
  })
  setBoardHoverClass()
  winningMessageElement.classList.remove('show')
}

function handleClick(e) {
  const cell = e.target
  const currentClass = circleTurn ? CIRCLE_CLASS : X_CLASS
  placeMark(cell, currentClass, sizeClass)
  if (checkWin(currentClass)) {
    endGame(false)
  } else if (isDraw()) {
    endGame(true)
  } else {
    swapTurns()
    setBoardHoverClass()

    // Computer makes its move
    if (circleTurn) {
      const bestMove = minimax([...cellElements], CIRCLE_CLASS).index;
      placeMark(cellElements[bestMove], CIRCLE_CLASS);
      if (checkWin(CIRCLE_CLASS)) {
        endGame(false);
      } else if (isDraw()) {
        endGame(true);
      } else {
        swapTurns();
        setBoardHoverClass();
      }
    }
  }
}

function endGame(draw) {
  if (draw) {
    winningMessageTextElement.innerText = 'Draw!'
  } else {
    winningMessageTextElement.innerText = `${circleTurn ? "O's" : "X's"} Wins!`
  }
  winningMessageElement.classList.add('show')
}

function isDraw() {
  return [...cellElements].every(cell => {
    return cell.classList.contains(X_CLASS) || cell.classList.contains(CIRCLE_CLASS)
  })
}

function placeMark(cell, currentClass, sizeClass) {
  const currentSize = getSize(cell);
  const newSize = getSizeFromClass(sizeClass);

  if (newSize >= currentSize || currentSize === -1) {
    cell.classList.remove(SIZE0_CLASS, SIZE1_CLASS, SIZE2_CLASS);
    cell.classList.remove(X_CLASS, CIRCLE_CLASS);
    cell.classList.add(sizeClass, currentClass);
  }
}

function getSize(cell) {
  if (cell.classList.contains(SIZE2_CLASS)) {return 2};  
  if (cell.classList.contains(SIZE1_CLASS)) {return 1};
  if (cell.classList.contains(SIZE0_CLASS)) {return 0};
  return -1;
}

function getSizeFromClass(sizeClass) {
  if (sizeClass === SIZE2_CLASS) {return 2};
  if (sizeClass === SIZE1_CLASS) {return 1};
  if (sizeClass === SIZE0_CLASS) {return 0};
  return -1;
}

function swapTurns() {
  circleTurn = !circleTurn
}

function setBoardHoverClass() {
  board.classList.remove(X_CLASS)
  board.classList.remove(CIRCLE_CLASS)
  if (circleTurn) {
    board.classList.add(CIRCLE_CLASS)
  } else {
    board.classList.add(X_CLASS)
  }
}

function checkWin(currentClass) {
  return WINNING_COMBINATIONS.some(combination => {
    return combination.every(index => {
      return cellElements[index].classList.contains(currentClass)
    })
  })
}

function minimax(newBoard, player) {
  const availableSpots = getAvailableSpots(newBoard);

  if (checkWin(X_CLASS)) {
    return { score: -10 };
  } else if (checkWin(CIRCLE_CLASS)) {
    return { score: 10 };
  } else if (availableSpots.length === 0) {
    return { score: 0 };
  }

  const moves = [];
  for (let i = 0; i < availableSpots.length; i++) {
    const move = {};
    move.index = availableSpots[i];
    newBoard[availableSpots[i]].classList.add(player);

    if (player === CIRCLE_CLASS) {
      const result = minimax(newBoard, X_CLASS);
      move.score = result.score;
    } else {
      const result = minimax(newBoard, CIRCLE_CLASS);
      move.score = result.score;
    }

    newBoard[availableSpots[i]].classList.remove(player);
    moves.push(move);
  }

  let bestMove;
  if (player === CIRCLE_CLASS) {
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


function getAvailableSpots(board) {
  return board.reduce((acc, cell, index) => {
    if (!cell.classList.contains(X_CLASS) && !cell.classList.contains(CIRCLE_CLASS)) {
      acc.push(index);
    }
    return acc;
  }, []);
}
