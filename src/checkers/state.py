from copy import deepcopy
from dataclasses import dataclass, field
from math import inf
from typing import Literal

Tile = Literal["b", "B", "r", "R", " "]


def new_board() -> list[str]:
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
    score: float = field(init=None)

    def __post_init__(self) -> None:
        self.score = self._count_score()

    def __str__(self) -> str:
        topbar = f"+-curr:{self.current_player}-+"
        btmbar = f"+-|{self.score: 4}|-+"
        result = "\n".join("|" + "".join(t for t in row) + "|" for row in self.board)
        return f"{topbar}\n{result}\n{btmbar}"

    def __eq__(self, other: "GameState") -> bool:
        if not isinstance(other, GameState):
            return False
        return self.board == other.board and self.current_player == other.current_player

    def __hash__(self) -> int:
        return hash(self.current_player + self.__str__())

    @staticmethod
    def _is_capture(dx: int, dy: int) -> bool:
        if max(abs(dx), abs(dy)) == 1:
            return False
        return True

    @property
    def opponent(self)->str:
        return "b" if self.current_player == "r" else "r"

    @staticmethod
    def in_bound(x: int , y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def bfs(self, x: int, y: int) -> list["GameState"]:
        next_capture_states = set()
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        q = [(self, x, y, False)]
        is_super = self.board[y][x].upper() == self.board[y][x]

        while q:
            current_game, curr_x, curr_y, has_captured = q.pop(0)
            capture_found = False
            for dx, dy in directions:
                nx, ny = curr_x + dx, curr_y + dy
                if (
                    self.in_bound(nx, ny)
                    and current_game.board[ny][nx].lower() == self.opponent
                    and self.in_bound(nx + dx, ny + dy)
                    and current_game.board[ny + dy][nx + dx] == " "
                    and (has_captured or (is_super or self.allowed_checker_y_direction() == dy))
                ):

                    q.append(
                        (
                            current_game.with_move(curr_x, curr_y, nx + dx, ny + dy),
                            nx + dx,
                            ny + dy,
                            True,
                        )
                    )
                    capture_found = True

            if not capture_found:
                if has_captured:
                    current_game.current_player = self.opponent
                    next_capture_states.add(current_game)

        return list(next_capture_states)

    def allowed_checker_y_direction(self) -> int:
        return -1 if self.current_player == "r" else 1

    def next_states(self) -> list["GameState"]:
        """
        Generate all possible game states by making all possible moves in one turn

        :return: list of all game states with next turn
        :rtype: GameState
        """
        next_possible_states: list["GameState"] = []
        has_to_capture = False
        next_moves = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

        for y in range(8):
            for x in range(8):
                if self.board[y][x] == " ":
                    continue
                tile_player = self.board[y][x].lower()
                is_super = self.board[y][x].upper() == self.board[y][x]
                if self.current_player != tile_player:
                    continue

                for dx, dy in next_moves:
                    nx, ny = x + dx, y + dy

                    if not self.in_bound(nx, ny):
                        continue

                    if (
                        self.board[ny][nx] == " "
                        and not has_to_capture
                        and (is_super or self.allowed_checker_y_direction() == dy)
                    ):
                        next_possible_states.append(self.with_move(x, y, nx, ny))

                    if (
                        self.board[ny][nx] != " "
                        and self.board[ny][nx].lower() == self.opponent
                    ):
                        next_captures_states = self.bfs(x, y)
                        if next_captures_states:
                            if has_to_capture:
                                next_possible_states.extend(next_captures_states)
                            else:
                                next_possible_states = next_captures_states
                                has_to_capture = True
                            break

        return next_possible_states

    def with_move(self, from_x: int, from_y: int, to_x: int, to_y: int) -> "GameState":
        """
        Creates a new game with the specified move. 
        If this move does not capture the enemy, the turn ends.

        :return: new game state after a move has been made
        """
        delta_x, delta_y = to_x - from_x, to_y - from_y

        new_state = deepcopy(self)
        if GameState._is_capture(delta_x, delta_y):
            mid_x, mid_y = from_x + delta_x // 2, from_y + delta_y // 2
            new_state.board[mid_y][mid_x] = " "
        else:
            new_state.current_player = self.opponent
        piece = self.board[from_y][from_x]
        new_state.board[to_y][to_x] = piece
        new_state.board[from_y][from_x] = " "

        if piece == "r" and to_y == 0:
            new_state.board[to_y][to_x] = "R"
        elif piece == "b" and to_y == 7:
            new_state.board[to_y][to_x] = "B"

        new_state.score = new_state._count_score()
        return new_state

    def _count_score(self) -> float:
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
        if r == 0 and R == 0:
            return -inf
        if b == 0 and B == 0:
            return inf
        score = (r - b) + (3 / 2) * (R - B)
        return score