from random_agent import RandomAgent

agent = RandomAgent("input6.txt")
print("----- load_data test ------")
agent.print_info()

print("----- predict_best_move of random agent test -----")
for i in range(5):
	move = agent.predict_best_move()
	print("random move = " + str(move))
	print("fruit type = " + agent.grid[move[0]][move[1]])
	point = agent.move(agent.grid, move[0], move[1])
	print("point = " + str(point))
	agent.print_info()

print()
