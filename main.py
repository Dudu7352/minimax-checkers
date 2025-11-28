from dataclasses import dataclass, field
from copy import deepcopy
from typing import Literal

Tile = Literal["r", "R", "b", "B", " "]


def new_board() -> list[list[Tile]]:
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
    current_player: Literal["r", "b"] = field(default="b")

    def repr_board(self) -> str:
        return "\n".join("".join(t for t in row) for row in self.board)

    @staticmethod
    def _is_move(dx: int, dy: int, move_length: int) -> bool:
        return move_length == abs(dx) == abs(dy)

    @property
    def opponent(self) -> str:
        return "r" if self.current_player == "b" else "b"

    def with_move(self, from_x: int, from_y: int, to_x: int, to_y) -> "GameState":
        if 0 <= from_y < 8 and 0 <= from_x < 8 and (from_x + from_y) % 2 == 0:
            raise ValueError(f"Incorrect from: {(from_x, from_y)}")
        if 0 <= to_y < 8 and 0 <= to_x < 8 and (to_x + to_y) % 2 == 0:
            raise ValueError(f"Incorrect to: {(to_x, to_y)}")
        if self.board[to_y][to_x] != " ":
            raise ValueError(
                f"Cannot move to a non-empty tile {(to_x, to_y)} which has value '{self.board[to_y][to_x]}'"
            )
        if self.board[from_y][from_x].lower() != self.current_player:
            raise ValueError(
                f"Cannot move from tile {(to_x, to_y)} on {self.current_player} turn (tile has value '{self.board[from_y][from_x]}')"
            )

        new_state: "GameState" | None = None
        delta_x, delta_y = to_x - from_x, to_y - from_y
        if GameState._is_move(delta_x, delta_y, move_length=1):
            new_state = deepcopy(self)
            new_state.board[from_y][from_x] = " "
            new_state.board[to_y][to_x] = self.board[from_y][from_x]

        elif GameState._is_move(delta_x, delta_y, move_length=2):
            mid_x, mid_y = (from_x + to_x) // 2, (from_y + to_y) // 2
            if self.board[mid_y][mid_x].lower() != self.opponent:
                raise ValueError(
                    f"Cannot jump over tile {(mid_x, mid_y)} which has value '{self.board[mid_y, mid_x]}'"
                )
            new_state = deepcopy(self)
            new_state.board[from_y][from_x] = " "
            new_state.board[mid_y][mid_x] = " "
            new_state.board[to_y][to_x] = self.board[from_y][from_x]

        if new_state is None:
            raise ValueError(
                f"Move from {(from_x, from_y)} to {(to_x, to_y)} cannot be made"
            )

        new_state.current_player = "b" if self.current_player == "r" else "r"

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


def main():
    game = GameState()
    print(game.repr_board())
    print("=" * 8)
    newgame = game.with_move(1, 2, 0, 3)
    print(newgame.repr_board())
    print("=" * 8)
    newgame = newgame.with_move(2, 5, 1, 4)
    print(newgame.repr_board())
    print("=" * 8)
    newgame = newgame.with_move(0, 3, 2, 5)
    print(newgame.repr_board())


if __name__ == "__main__":
    main()
