""""
Requirments:
1. Board -> Array of '_'
2. Players -> 'x' and 'o'
3. Function for make move
4. Function for checking what moves can be made -> If no more moves left, check conditions
5. Check game condition (win, lose, draw)
6. ?? Function to check who's turn it is
7. Function to determine what move to make
8. Eng game funciton -> Say who the winner is and stuff

Logic:
1. Grab all the available moves
2. Determine game state
    If winner:
        return call end_game_function winner and loser
    If no more moves
        return call_end_game_function draw
3. Check who's turn it is
4. Determine what move to make 
5. Make move


0 1 2
3 4 5
6 7 8
"""

from hmac import new
import random
from typing import Literal, Union

starting_board = ["x", "_", "_", "x", "_", "_", "_", "_", "_"]


class Game:
    GameMode = Literal["h vs h", "easy ai", "easy_ai vs easy_ai"]
    Players = Literal["x", "o"]

    current_player: Players = "x"
    board = ["_" for i in range(9)]
    win_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    def __init__(
        self,
        human_player: Players = "x",
        game_mode: GameMode = "easy ai",
        starting_board: list[str] = board,
    ) -> None:
        self.human_player = human_player
        self.game_mode = game_mode
        self.board = starting_board

        self.legal_moves: list[int] = self.__set_new_legal_moves(starting_board)

    def start(self):
        while True:
            winner = self.__get_winner(self.board)

            if winner != None:
                self.__call_end_game(winner)
                break
            if len(self.legal_moves) == 0:
                self.__call_end_game(None)
                break

            next_move = self.__get_next_move(self.current_player)

            self.make_move(next_move, self.board)

    def __set_new_legal_moves(self, board: list[str]) -> list[int]:
        new_legal_moves = []
        for index, place in enumerate(board):
            if place == "_":
                new_legal_moves.append(index)

        self.legal_moves = new_legal_moves
        return new_legal_moves

    def __get_winner(self, board: list[str]) -> Union[Players, None]:
        for win_condition in self.win_conditions:
            good_var = (
                board[win_condition[0]]
                + board[win_condition[1]]
                + board[win_condition[2]]
            )
            if good_var == "xxx":
                return "x"
            if good_var == "ooo":
                return "o"
        return None

    def __call_end_game(self, winner: Union[str, None]) -> None:
        if winner == None:
            print("The game is a draw")
        else:
            print(f"The winner is {winner}")

    def __get_ai_next_move(self, board: list[str], current_player: Players) -> int:
        ai_move = random.choice(self.legal_moves)
        return ai_move

    def __get_next_move(self, current_player: Players):
        if self.game_mode == "easy_ai vs easy_ai":
            return self.__get_ai_next_move(self.board, current_player)
        elif current_player == self.human_player or self.game_mode == "h vs h":
            return self.__get_user_move()
        else:
            return self.__get_ai_next_move(self.board, current_player)

    def make_move(self, move: int, new_board: list[str] = board) -> list[str]:
        new_board[move] = self.current_player
        self.__print_the_board(new_board)

        self.current_player = self.__get_next_player(self.current_player)
        self.board = new_board
        self.__set_new_legal_moves(new_board)
        return new_board

    def __print_the_board(self, board: list[str]) -> None:
        print(f"{board[0]} {board[1]} {board[2]}")
        print(f"{board[3]} {board[4]} {board[5]}")
        print(f"{board[6]} {board[7]} {board[8]}")
        print("\n\n")

    def __get_next_player(self, current_player: Players) -> Players:
        if current_player == "o":
            return "x"
        return "o"

    def __get_user_move(self) -> int:
        print("\033[93m\033[1m >> \033[0m", "Make a move")
        print(f"\033[93m\033[1m >> \033[0m Available moves are {self.legal_moves}")
        self.__print_the_board(self.board)

        user_move = input("Player input: ")

        if int(user_move) not in self.legal_moves:
            print("Bad move")
            print(f"Available moves are {self.legal_moves}")
            return self.__get_user_move()
        return int(user_move)


new_game = Game("x", "easy_ai vs easy_ai")
new_game.start()
