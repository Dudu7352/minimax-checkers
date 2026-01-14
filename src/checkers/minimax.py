from checkers.node import GameNode
from checkers.print import side_by_side
from checkers.state import GameState


class MiniMaxGameBot:
    tree_depth: int
    root: "GameNode"

    def __init__(self, root_node: "GameNode", tree_depth: int) -> None:
        self.root: "GameNode" = root_node
        self.tree_depth: int = tree_depth
    
    def minimax_move(self, first_move: bool, root_state: "GameState | None") -> GameState | None:
        if not first_move:
            self.root.init_children()
            assert self.root.children is not None
            for child in self.root.children:
                if child.state == root_state:
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
        return self.root.state

    def dfs(self, node: "GameNode", stack: list["GameState"], possible_paths: list[list["GameState"]]) -> None:
        stack.append(node.state)
        if not node.children:
            possible_paths.append(list(stack))
        else:
            for child in node.children:
                self.dfs(child, stack, possible_paths)
        stack.pop()

    def print_paths(self) -> None:
        possible_paths = []
        self.dfs(self.root, [], possible_paths)
        for path in possible_paths:
            possible = [board.__str__() for board in path]
            print(side_by_side(*possible))
            print("\n")

