from copy import deepcopy
from dataclasses import dataclass, field
from typing import Literal

Tile = Literal['b','B','r','R',' ']

def new_board() -> list[str]:#correct
    board = list()
    board.append(list(" b b b b"))
    board.append(list("b b b b "))
    board.append(list(" b b b b"))
    board.append(list(8 * " "))
    board.append(list(8 * " "))
    board.append(list("r r r r "))
    board.append(list(" r r r r"))
    board.append(list("r r r r "))
    return board

@dataclass
class GameState:
    board: list[list[Tile]] = field(default_factory=new_board)
    current_player: Literal['r','b'] = field(default='b')

    def repr_board(self) -> str:
        return "\n".join("".join(t for t in row) for row in self.board)

    @staticmethod
    def _is_diagonal(dx: int, dy: int) -> bool:
        return abs(dx) == abs(dy)
        #sprawdzanie czy mozna dojsc do miejsca x,y, trzeba bedzie jakos zrobić funkcje która
        #sprawdza czy da sie w ogole dojsc na te pole uzywając tego skośnego chodzenia
    
    @staticmethod
    def _is_capture(dx: int, dy: int) -> bool:#added
        return max(abs(dx),abs(dy))>1
        #sprawdza czy ruch jest biciem

    @property
    def opponent(self):
        return 'b' if self.current_player == 'r' else 'r'
    
    def with_moves(self, from_x: int, from_y: int, to_x: int, to_y) -> "GameState":
        if from_x < 0 or from_x > 7 or from_y < 0 or from_y > 7 or (from_x + from_y)%2==0:#corrected
            raise ValueError(f"Incorrect from: {(from_x, from_y)}")
        if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7 or (to_x + to_y)%2==0:
            raise ValueError(f"Incorrect from: {(to_x, to_y)}")
        if from_x == to_x and from_y == to_y:#added
            raise ValueError(f"Tried to go to the same place")
        if self.board[to_y][to_x] != " ":
            raise ValueError(
                f"Cannot move to a non-empty tile {(to_x, to_y)} which has value '{self.board[to_y][to_x]}'"
            )
        if self.board[from_y][from_x].lower() != self.current_player:
            raise ValueError(
                f"Cannot move from tile {(to_x, to_y)} on {self.current_player} turn (tile has value '{self.board[from_y][from_x]}')"
            )
        delta_x, delta_y = to_x - from_x, to_y - from_y

        new_state: 'GameState' | None = None

        if not GameState._is_capture(delta_x, delta_y):
            #tu musi byc jakas funkcja ktora sprawdza czy ten ruch jest mozliwy
            new_state = deepcopy(self)
            new_state.board[to_y][to_x] = self.board[from_y][from_x]
            new_state.board[from_y][from_x] = " "
            
            if new_state.board[from_y][from_x] == " ":
                new_state.current_player = "b" if self.current_player == "r" else "r"
                #jezeli udalo sie zrobic ruch to zamieniamy gracza
        else:
            #tu musi byc jakas funkcja ktora sprawdza czy ten ruch jest mozliwy
            new_state = deepcopy(self)
            new_state.board[to_y][to_x] = self.board[from_y][from_x]
            new_state.board[from_y][from_x] = " "
            
            if new_state.board[from_y][from_x] == " ":
                new_state.current_player = "b" if self.current_player == "r" else "r"
                #jezeli udalo sie zrobic ruch to zamieniamy gracza
        
        if new_state is None:
            raise ValueError(
                f"Move from {(from_x, from_y)} to {(to_x, to_y)} cannot be made"
            )

        return new_state

    def count_score(self) -> float:
        r = R = b = B = 0
        for row in self.board:
            for tile in row:
                if tile == " ":
                    continue
                elif tile == "r":
                    r += 1
                elif tile == "R":
                    R += 1
                elif tile == "b":
                    b += 1
                elif tile == "B":
                    B += 1
                else:
                    raise ValueError("Unexpected element on the board")
        score = (r - b) + (3 / 2) * (R - B)
        return score


