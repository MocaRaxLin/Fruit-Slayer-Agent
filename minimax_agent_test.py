from minimax_agent import MinimaxAgent
import time

s = time.time()

agent = MinimaxAgent("test_input.txt")
print("----- load_data test ------")
agent.print_info()

print("----- predict_best_move of minimax agent with 3 depth test -----")
move = agent.predict_best_move(3) # test on depth = 3, about 25 secs
print("best move = " + str(move))
print("minimax points to expect to get = " + str(agent.minimax_root.best))
print("next grid = ")
agent.print_grid(agent.minimax_root.next_state.grid)

print("----- write_grid test ------")
agent.write_next_grid("test_output_minimax.txt")
print("see test_output.txt in folder!") #E4
print("It should be the same as next gird")
print()

print("Process time is: ")
print(time.time() - s)
print("secs")