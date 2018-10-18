from random_agent import RandomAgent

agent = RandomAgent("test_input.txt")
print("----- load_data test ------")
agent.print_info()

print("----- move test ------")
points = agent.move(4, 7)
print("points = " + str(points)) # 14*14 = 196
agent.print_info()

print("----- write_grid test ------")
agent.write_grid("test_output.txt", 4, 7)
print("see test_output.txt in folder!") #I5
print()

print("----- predict_best_move of random agent test -----")
for i in range(5):
	move = agent.predict_best_move()
	print("random move = " + str(move))
	point = agent.move(move[0], move[1])
	print("point = " + str(point))
	agent.print_info()

print()
