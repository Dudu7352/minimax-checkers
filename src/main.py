from checkers import GameNode, GameState, MiniMaxGameBot, new_board
from checkers import side_by_side
from checkers.random import RandomBot
from math import inf
import time

if __name__ == "__main__":
    # times = []
    # for i in range(2,3):
    #     bot1 = MiniMaxGameBot(GameNode(GameState(), 0), 4)  # b player
    #     bot2 = MiniMaxGameBot(GameNode(GameState(), 0), 4)  
    #     #randomBot = RandomBot(seed=42) # r player
    #     #start = time.time()
    #     bot1.root.state.current_player = "b"
    #     child_state_1 = bot1.minimax_move(True, None)
    #     print(str(child_state_1))
    #     bot1.print_paths()
    #     #print(side_by_side(*[str(i) for i in plan]))
    # """
    # game=GameState()
    # print(game)
    # while True:
    #     game=GameState()
    #     bot1 = MiniMaxGameBot(GameNode(game, 0), 6)  # b player
        
    #     # for state in game.next_states():
    #     #     print(state)
    #     game = bot1.minimax_move(True, None)
        
        
    # moves = 0
    bot1 = MiniMaxGameBot(GameNode(GameState(), 0), 4)  # b player
    bot2 = MiniMaxGameBot(GameNode(GameState(), 0), 4) 
    child_state_1 = bot1.minimax_move(True, None)
    
    while True:
        child_state_2 = bot2.minimax_move(False, child_state_1)
        if not child_state_2:
            break
        print(str(child_state_2))
        child_state_1 = bot1.minimax_move(False, child_state_2)
        
        if not child_state_1:
            break
        print(str(child_state_1))
        
        if abs(child_state_1.score) == inf or abs(child_state_2.score) == inf:
            break
        
    print("game over")
    # end = time.time()
  #  times.append(end - start)
 #   print(f"{i} : {end-start}")
#print(times)
