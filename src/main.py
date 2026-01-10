from checkers import GameNode, GameState, MiniMaxGameBot, new_board
from checkers.random import RandomBot

if __name__ == "__main__":
    bot1 = MiniMaxGameBot(GameNode(GameState(new_board()), 0), 2)  # b player
    bot2 = MiniMaxGameBot(GameNode(GameState(new_board()), 0), 3)  
    randomBot = RandomBot(seed=42) # r player
    
    child_state_1 = bot1.minimax_move(True, None)
    print(str(child_state_1))

    while True:
        child_state_2 = randomBot.random_move(child_state_1)
        if not child_state_2:
            break
        print(str(child_state_2))
        child_state_1 = bot1.minimax_move(False, child_state_2)
        
        if not child_state_1:
            break
        print(str(child_state_1))
        
        
        
    print("game over")
