from dataclasses import dataclass, field
from math import inf
from checkers.state import GameState

@dataclass
class GameNode:
    state: "GameState"
    node_depth: int
    children: list["GameNode"] | None = field(default=None)

    def __hash__(self) -> None:
        return self.state.__hash__()

    def __eq__(self, other: "GameState"):
        if not isinstance(other, GameNode):
            return False
        return self.state == other.state
    
    def __str__(self) -> str:
        return self.state.__str__()

    def init_children(self) -> None:
        if self.children is None:
            self.children = [
                GameNode(state, self.node_depth + 1)
                for state in self.state.next_states()
            ]

    def best_minimax(
        self, maximizing_player: bool, tree_depth: int, alpha: float = -inf, beta: float = inf
    ) -> tuple[int, "GameNode | None"]:
        if self.node_depth > tree_depth or abs(self.state.score) == inf:
            return self.state.score, None  # score and GameNode
        
        self.init_children()

        if not self.children:
            return self.state.score, None

        if maximizing_player:
            best_score = -inf
            best_child = None
            for child in self.children:
                score, _ = child.best_minimax(not maximizing_player, tree_depth, alpha, beta)
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
                score, _ = child.best_minimax(not maximizing_player, tree_depth, alpha, beta)
                if best_score >= score:
                    best_score = score
                    best_child = child
                beta = min(best_score, beta)
                if alpha >= beta:
                   break
            return best_score, best_child