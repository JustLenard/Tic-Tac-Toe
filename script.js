const dificultyChoices = document.querySelector('#dropdown-options');
const markerChoices = document.querySelectorAll('.marker');
const playingField = document.querySelectorAll('.position');
const restartBtn = document.querySelectorAll('.restart');
const endGameModal = document.querySelector('.end-game-modal');
const winningMessage = document.querySelector('.winning-message');
const winConditions = [
	[0, 1, 2],
	[3, 4, 5],
	[6, 7, 8],
	[0, 3, 6],
	[1, 4, 7],
	[2, 5, 8],
	[0, 4, 8],
	[6, 4, 2],
];
var player = 'x';
var ai = '○'; // This is actually HTML circle and not 'o' neither '0'
const internalBoard = ['_', '_', '_', '_', '_', '_', '_', '_', '_'];

// Restarts the game if dificutly is changed
dificultyChoices.addEventListener('change', () => {
	restart();
});

// Event listener for restart buttons
restartBtn.forEach(button => {
	button.addEventListener('click', () => {
		restart();
	});
});

//Marker choice ('○' or 'x')
markerChoices.forEach(choice => {
	choice.addEventListener('click', () => {
		markerChoices.forEach(choice => {
			choice.classList.remove('active');
		});
		choice.classList.add('active');
		player = choice.textContent.normalize().replace(/\s/g, '');
		ai = getOpponent(player);
		restart();
	});
});

//Player move
playingField.forEach(emptySqaure => {
	emptySqaure.addEventListener('click', () => {
		playingField.forEach(emptySqaure => {
			emptySqaure.classList.remove('active');
		});
		if (emptySqaure.textContent === '') {
			emptySqaure.classList.add('active');
			emptySqaure.textContent = player;
			checkEndGame(internalBoard);
			if (getLegalMoves(internalBoard).length !== 0) {
				aiMove = useCorrectAiDifficulty();
				playingField[aiMove].textContent = ai;
				checkEndGame(internalBoard);
			}
		}
	});
});

// Use the ai with the correct dificulty
function useCorrectAiDifficulty() {
	if (dificultyChoices.value === 'easy') {
		return easyAi();
	} else if (dificultyChoices.value === 'normal') {
		return normalAi(internalBoard, ai);
	} else if (dificultyChoices.value === 'impossible') {
		return minimaxAi(internalBoard, ai);
	}
}

// Easy Ai
function easyAi() {
	let legalMoves = getLegalMoves(internalBoard);
	let randNum = randomNumber(legalMoves.length);
	return legalMoves[randNum];
}

// Normal Ai
function normalAi(board, currentPlayer) {
	if (randomNumber(10) > 3) {
		return minimaxAi(board, currentPlayer);
	} else {
		return easyAi();
	}
}

// Impossible Ai
function minimaxAi(board, currentPlayer) {
	let bestMove = undefined;
	let bestScore = undefined;
	let legalMoves = getLegalMoves(board);
	legalMoves.forEach(legalMove => {
		newBoard = makeMove(board, currentPlayer, legalMove);
		opponet = getOpponent(currentPlayer);
		score = minimax(newBoard, opponet);
		board[legalMove] = '_';

		if (bestScore === undefined || score > bestScore) {
			bestScore = score;
			bestMove = legalMove;
		}
	});
	return bestMove;
}

function minimax(board, currentPlayer) {
	let legalMoves = getLegalMoves(board);
	let winnerScore = checkWinner(board);
	if (winnerScore !== 0) {
		return checkWinner(board);
	}
	if (legalMoves.length === 0) {
		return 0;
	}

	var scores = [];

	legalMoves.forEach(legalMove => {
		newBoard = makeMove(board, currentPlayer, legalMove);
		opponet = getOpponent(currentPlayer);
		let score = minimax(newBoard, opponet);
		scores.push(score);
		board[legalMove] = '_';
	});
	if (currentPlayer === player) {
		return Math.min(...scores);
	} else {
		return Math.max(...scores);
	}
}

//Update the internal board for AI to work with
function updateInternalBoard(internalBoard) {
	for (var i = 0; i < 9; i++) {
		if (playingField[i].textContent === '') {
			internalBoard[i] = '_';
		} else {
			internalBoard[i] = playingField[i].textContent;
		}
	}
}

// Get all the legal moves
function getLegalMoves(board) {
	let legalMoves = [];
	for (let i = 0; i < 9; i++) {
		if (board[i] === '_') {
			legalMoves.push(i);
		}
	}
	return legalMoves;
}

// Let the ai make a move
function makeMove(board, currentPlayer, position) {
	board[position] = currentPlayer;
	return board;
}

// Find who is the opponent
function getOpponent(currentPlayer) {
	if (currentPlayer === '○') {
		return 'x';
	} else if (currentPlayer === 'x') {
		return '○';
	}
}

// Look for a winner in the interanl board for the ai to work with
function checkWinner(board) {
	let points = 0;
	winConditions.forEach(condition => {
		if (
			board[condition[0]] + board[condition[1]] + board[condition[2]] ===
			ai + ai + ai
		) {
			points = 10;
		} else if (
			board[condition[0]] + board[condition[1]] + board[condition[2]] ===
			player + player + player
		) {
			points = -10;
		}
	});
	return points;
}

//Check for end game (win, lose or tie) on the actual board
function checkEndGame(board) {
	updateInternalBoard(internalBoard);
	if (checkWinner(board) !== 0) {
		if (checkWinner(board) === 10) {
			callEndGameModal(ai);
		} else {
			callEndGameModal(player);
		}
	} else if (getLegalMoves(board).length === 0) {
		callEndGameModal('tie');
	}
}

//Handle Game Over
function callEndGameModal(winner) {
	if (winner === 'tie') {
		winningMessage.textContent = `The game is a Tie`;
	} else {
		winningMessage.textContent = `The winner is ${winner}`;
	}
	endGameModal.classList.add('show');
}

// Restart function
function restart() {
	playingField.forEach(emptySquare => {
		emptySquare.classList.remove('active');
		emptySquare.textContent = '';
	});
	endGameModal.classList.remove('show');
	if (player !== 'x') {
		playingField[randomNumber(9)].textContent = ai;
	}
}

//Random number
function randomNumber(length) {
	return Math.floor(Math.random() * length);
}
