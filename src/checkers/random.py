import random
from checkers.state import GameState


class RandomBot:
    def __init__(self, seed: int) -> None:
        self.random = random.Random(seed)

    def random_move(self, root_state: "GameState") -> "GameState | None":
        next_states = root_state.next_states()
        if not next_states:
            return None
        
        return self.random.choice(next_states)
