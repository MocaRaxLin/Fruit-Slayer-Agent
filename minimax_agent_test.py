from minimax_agent import MinimaxAgent
import time

s = time.time()

agent = MinimaxAgent("input4.txt")
print("----- load_data test ------")
agent.print_info()

depth = 3
print("----- predict_best_move of minimax agent with "+str(depth)+" depth test -----")
move = agent.predict_best_move(depth) # test on depth = 3, about 25 secs
print("best move = " + str(move))
print("minimax points to expect to get = " + str(agent.minimax_root.best))
print("next grid = ")
agent.print_grid(agent.minimax_root.next_state.grid)

# agent.print_minimax()

print("----- write_grid test ------")
agent.write_next_grid("test_output4_minimax.txt")
print("see test_output.txt in folder!")
print()

print("Searched node: " + str(agent.searched_node))
e = time.time() - s
print("Process time: "+str(e)+" secs")
print("average time per node: "+str(e/agent.searched_node))
print()