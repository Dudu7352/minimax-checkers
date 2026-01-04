from copy import deepcopy
from dataclasses import dataclass, field
from typing import Literal
from math import inf

Tile = Literal["b", "B", "r", "R", " "]
"""
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
"""


def new_board() -> list[str]:
    board = list()
    board.append(list("        "))
    board.append(list("b b     "))
    board.append(list(" b      "))
    board.append(list("r       "))
    board.append(list("        "))
    board.append(list("        "))
    board.append(list("        "))
    board.append(list("        "))
    return board


class MiniMaxGameTree:
    depth: int
    root: "GameNode"

    def __init__(self, root_state: "GameNode", depth: int) -> None:
        self.root: "GameNode" = root_state
        self.depth = depth

    def minimax_move(self, maximize: Literal["r", "b"]) -> None:
        score, best_child = self.root.best_minimax(
            self.root.depth + self.depth, maximize
        )
        print(f"best move has {score=}")
        self.root = best_child


def side_by_side(*strs: list[str]):
    str_arrs = [s.split("\n") for s in strs]
    result = ""
    for i in range(len(str_arrs[0])):
        result += "    ".join(s[i] for s in str_arrs)
        result += "\n"
    return result


@dataclass
class GameNode:
    state: "GameState"
    depth: int
    children: list["GameNode"] | None = field(default=None)

    def __init__(self, state, new_depth):
        self.depth = new_depth
        self.state = state
        self.children = None

    # def populate_with_depth(self, max_depth: int) -> None:
    #     if max_depth <= self.depth:
    #         return
    #     if self.children is None:
    #         self.children = [GameNode(state, self.depth+1) for state in self.state.next_states()]
    #     for child in self.children:
    #         child.populate_with_depth(max_depth)

    def best_minimax(
        self, max_depth: int, maximize: Literal["r", "b"]
    ) -> tuple[int, "GameNode | None"]:
        if max_depth == self.depth:
            return self.state.score, self

        if self.children is None:
            self.children = [
                GameNode(state, self.depth + 1) for state in self.state.next_states()
            ]

        best_score: float | None = inf * (1 if maximize == "b" else -1)
        best_child: "GameNode" | None = None
        for child in self.children:
            child_score, _ = child.best_minimax(
                max_depth, "r" if maximize == "b" else "b"
            )
            is_score_better = best_score < child_score
            if maximize != "r":
                is_score_better = best_score > child_score
            if best_score is None or is_score_better:
                best_score = child_score
                best_child = child
        return best_score, best_child


@dataclass
class GameState:
    board: list[list[Tile]] = field(default_factory=new_board)
    current_player: Literal["r", "b"] = field(default="b")
    score: float = field(init=None)

    def __post_init__(self) -> None:
        self.score = self._count_score()

    def repr_board(self) -> str:
        topbar = f"+-curr:{self.current_player}-+"
        btmbar = "+--------+"
        result = "\n".join("|" + "".join(t for t in row) + "|" for row in self.board)
        return f"{topbar}\n{result}\n{btmbar}"

    def __hash__(self):
        return hash(self.current_player + self.repr_board())

    @staticmethod
    def _is_diagonal(dx: int, dy: int) -> bool:
        return abs(dx) == abs(dy)
        # sprawdzanie czy mozna dojsc do miejsca x,y, trzeba bedzie jakos zrobić funkcje która
        # sprawdza czy da sie w ogole dojsc na te pole uzywając tego skośnego chodzenia

    @staticmethod
    def _is_capture(dx: int, dy: int) -> bool:  # added
        if max(abs(dx), abs(dy)) == 1:
            return False
        return True
        # sprawdza czy ruch jest biciem

    @property
    def opponent(self):
        return "b" if self.current_player == "r" else "r"

    def canMoveOneTile(
        self, from_x: int, from_y: int, to_x: int, to_y: int, figure: chr
    ):
        if figure == "b":
            return from_x < to_x
        if figure == "r":
            return from_x > to_x
        return True

    @staticmethod
    def in_bound(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def bfs(self, x, y) -> list["GameState"]:
        next_capture_states: set["GameState"] = set()
        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        q = [(self, x, y, False)]

        while q:
            current_game, curr_x, curr_y, has_captured = q.pop(0)
            capture_found = False
            for dx, dy in directions:
                nx, ny = curr_x + dx, curr_y+dy
                if GameState.in_bound(nx, ny) and current_game.board[ny][nx].lower() == self.opponent and GameState.in_bound(nx+dx, ny+dy) and current_game.board[ny+dy][nx+dx] == ' ':
                    print(current_game.repr_board())
                    q.append((current_game.with_move(curr_x, curr_y, nx+dx, ny+dy), nx+dx, ny+dy, True))
                    print(current_game.repr_board())
                    capture_found = True
                    
            if not capture_found:
                if has_captured:
                    print("!!!")
                    current_game.current_player = current_game.opponent
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
        # generalnie wymagania są takie:
        # 1. działa
        next_possible_states: list["GameState"] = []
        has_to_capture = False
        next_moves = [[-1,-1], [-1, 1], [1,1], [1,-1]]
        
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == " ":
                    continue
                tile_player = self.board[y][x].lower()
                is_super = self.board[y][x].upper() == self.board[y][x]
                if self.current_player != tile_player:
                    continue
                
                for dx, dy in next_moves:
                    nx, ny = x+dx, y+dy

                    if not GameState.in_bound(nx, ny):
                        continue

                    if self.board[ny][nx] == " " \
                       and not has_to_capture \
                       and (is_super or self.allowed_checker_y_direction() == dy):
                        next_possible_states.append(self.with_move(x, y, nx, ny))
                    
                    if self.board[ny][nx] != " " and self.board[ny][nx].lower() == self.opponent:
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
        Perform a valid move and
        """
        delta_x, delta_y = to_x - from_x, to_y - from_y

        new_state = deepcopy(self)
        if GameState._is_capture(delta_x, delta_y):
            mid_x, mid_y = from_x + delta_x // 2, from_y + delta_y // 2
            new_state.board[mid_y][mid_x] = " " 
        else:
            new_state.current_player = self.opponent
        
        new_state.board[to_y][to_x] = new_state.board[from_y][from_x]
        new_state.board[from_y][from_x] = " "
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


if __name__ == "__main__":
    nodeusz = GameNode(GameState(), 0)
    print(nodeusz.state.current_player)
    print(id(nodeusz.state))
    for state in nodeusz.state.next_states():
        print(state.repr_board())
    # tree = MiniMaxGameTree(nodeusz, 3)
    # del nodeusz
    # print(tree.root.state.repr_board())
    # print(f"score={tree.root.state.score}")
    # for child in tree.root.state.next_states():
    #     for grandchild in child.next_states():
    #         for grandgrandchild in grandchild.next_states():
    #             print(
    #                 side_by_side(
    #                     tree.root.state.repr_board(),
    #                     child.repr_board(),
    #                     grandchild.repr_board(),
    #                     grandgrandchild.repr_board(),
    #                 )
    #             )
    #             print("Stats: ", end="")
    #             grandgrandchild._count_score()
    #             print(f"Score: {grandgrandchild.score=}")
    # print("======")
    # print(tree.root.state.repr_board())
    # tree.minimax_move(maximize="b")
    # print("======")
    # print(tree.root.state.repr_board())
