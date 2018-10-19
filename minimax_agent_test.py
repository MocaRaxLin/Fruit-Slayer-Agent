from minimax_agent import MinimaxAgent

agent = MinimaxAgent("test_input.txt")
print("----- load_data test ------")
agent.print_info()

print("----- move test ------")
points = agent.move(agent.grid, 4, 7)
print("points = " + str(points)) # 14*14 = 196
agent.print_info()

print("----- write_grid test ------")
agent.write_grid("test_output.txt", 4, 7)
print("see test_output.txt in folder!") #I5
print()

print("----- predict_best_move of minimax agent with 2 depth test -----")
move = agent.predict_best_move(2) # test on depth = 2
print("best move = " + str(move))
agent.print_minimax()

print()