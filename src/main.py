from checkers import GameNode, GameState, MiniMaxGameTree, new_board
from math import inf

if __name__ == "__main__":
    bot1 = MiniMaxGameTree(GameNode(GameState(new_board()), 0), 6)  # b player
    bot2 = MiniMaxGameTree(GameNode(GameState(new_board()), 0), 3)  # r player

    child_node_1 = bot1.minimax_move(True, None)
    print(str(child_node_1.state))

    while True:
        child_node_2 = bot2.minimax_move(False, child_node_1)
        if not child_node_2:
            break
        print(str(child_node_2.state))
        child_node_1 = bot1.minimax_move(False, child_node_2)
        
        if not child_node_1:
            break
        print(str(child_node_1.state))
        
        if abs(child_node_2.state.score) == inf or abs(child_node_1.state.score) == inf:
            break
        
    print("game over")
