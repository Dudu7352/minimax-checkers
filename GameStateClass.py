from copy import deepcopy
from dataclasses import dataclass, field
from typing import Literal
import math
from math import inf


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




class MiniMaxGameTree:
    tree_depth: int
    root: "GameNode"

    def __init__(self, root_node: "GameNode", tree_depth: int) -> None:
        self.root: "GameNode" = root_node
        self.tree_depth = tree_depth

    def minimax_move(self, first_move, root_node) -> "GameNode":
        if not first_move:
            self.root.init_children()
            for child in self.root.children:
                if child == root_node:
                    self.root = child
                    break
            else:
                raise Exception("No such state in the tree")

        _, best_child = self.root.best_minimax(
            self.root.state.current_player == "r",
            self.tree_depth + self.root.node_depth,
        )

        if not best_child:
            return None

        self.root = best_child
        return self.root

    def dfs(self, node: "GameNode", stack, possible_paths):
        stack.append(node.state)
        if not node.children:
            possible_paths.append(list(stack))
        else:
            for child in node.children:
                self.dfs(child, stack, possible_paths)
        stack.pop()

    def print_paths(self):
        possible_paths = []
        self.dfs(self.root, [], possible_paths)
        for path in possible_paths:
            possible = [board.repr_board() for board in path]
            print(side_by_side(*possible))
            print("\n")
        


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
    node_depth: int
    children: list["GameNode"] | None = field(default=None)

    def __init__(self, state, node_depth):
        self.node_depth = node_depth
        self.state = state
        self.children = None

    def __hash__(self):
        return self.state.__hash__()

    def __eq__(self, other):
        if not isinstance(other, GameNode):
            return False
        return self.state == other.state

    def init_children(self) -> None:
        if self.children is None:
            self.children = [
                GameNode(state, self.node_depth + 1)
                for state in self.state.next_states()
            ]

    def best_minimax(
        self, maximizingPlayer, tree_depth: int, alpha: float = -inf, beta: float = inf
    ) -> tuple[int, "GameNode | None"]:
        if self.node_depth > tree_depth or abs(self.state.score) == inf:
            return self.state.score, None  # score and GameNode
        
        self.init_children()

        if not self.children:
            return self.state.score, None

        if maximizingPlayer:
            best_score = -inf
            best_child = None
            for child in self.children:
                score, _ = child.best_minimax(not maximizingPlayer, tree_depth, alpha, beta)
                if best_score <= score:
                    best_score = score
                    best_child = child
                alpha = max(best_score, alpha)
                if alpha >= beta:
                   break
            return best_score, best_child
        else:
            best_score = inf
            best_child = None
            for child in self.children:
                score, _ = child.best_minimax(not maximizingPlayer, tree_depth, alpha, beta)
                if best_score >= score:
                    best_score = score
                    best_child = child
                beta = min(best_score, beta)
                if alpha >= beta:
                   break
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
        btmbar = f"+- {self.score}--+"
        result = "\n".join("|" + "".join(t for t in row) + "|" for row in self.board)
        return f"{topbar}\n{result}\n{btmbar}"

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return False
        return self.board == other.board and self.current_player == other.current_player

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
        # generalnie wymagania są takie:
        # 1. działa
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
        Perform a valid move and
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
    
if __name__ == "__main__":
    bot1 = MiniMaxGameTree(GameNode(GameState(new_board()), 0), 6)  # b player
    bot2 = MiniMaxGameTree(GameNode(GameState(new_board()), 0), 3)  # r player

    child_node_1 = bot1.minimax_move(True, None)
    print(child_node_1.state.repr_board())

    while True:
        child_node_2 = bot2.minimax_move(False, child_node_1)
        if not child_node_2:
            break
        print("after bot2 move:\n", child_node_2.state.repr_board())
        # bot2.print_paths()
        child_node_1 = bot1.minimax_move(False, child_node_2)
        
        if not child_node_1:
            break
        print("after move bot1:\n", child_node_1.state.repr_board())
        # bot1.print_paths()
        if abs(child_node_2.state.score) == inf or abs(child_node_1.state.score) == inf:
            break
        
    print("game over")
