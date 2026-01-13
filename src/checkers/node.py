from dataclasses import dataclass, field
from math import inf
from checkers.state import GameState
import random

@dataclass
class GameNode:
    state: "GameState"
    node_depth: int
    children: list["GameNode"] | None = field(default=None)

    def __hash__(self) -> int:
        return self.state.__hash__()

    def __eq__(self, other: object):
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
            
            random.shuffle(self.children)

    def best_minimax(
        self, maximizing_player: bool, tree_depth: int, alpha: float = -inf, beta: float = inf
    ) -> tuple[float, "GameNode | None"]:
        if abs(self.state.score) == inf:

            if self.state.score > 0:
                return 100_000 - self.node_depth, None
            else: 
                return -100_000 + self.node_depth, None

        if self.node_depth >= tree_depth:
            return self.state.score, None
        
        self.init_children()

        if not self.children:
            return self.state.score, None

        best_child = self.children[0]
        
        if maximizing_player:
            best_score = -inf
            for child in self.children:
                score, _ = child.best_minimax(not maximizing_player, tree_depth, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_child = child
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break
            return best_score, best_child
        else:
            best_score = inf
            for child in self.children:
                score, _= child.best_minimax(not maximizing_player, tree_depth, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_child = child
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break
            return best_score, best_child
    

    