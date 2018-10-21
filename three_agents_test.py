import time
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from minimax_ab_agent import MinimaxAgentPruning

def dfs(grid, r, c, N, p):
	if r == -1 or c == -1 or r == N or c == N or grid[r][c] != p:
		return
	grid[r][c] = '*'
	dfs(grid, r-1, c, N, p)
	dfs(grid, r+1, c, N, p)
	dfs(grid, r, c-1, N, p)
	dfs(grid, r, c+1, N, p)
	return

def getIdx(move:str):
	c = ord(move[0]) - ord('A')
	r = int(move[1:]) - 1
	return [r, c]

def verify(no:int, correct_file:str, test_file:str):
	f1 = open(correct_file, mode='r')
	f2 = open(test_file, mode='r')
	lines1 = f1.readlines()
	lines2 = f2.readlines()
	f1.close()
	f2.close()
	grid1 = []
	for i in range(3, len(lines1)):
		line = list(lines1[i])
		grid1.append(line)

	move = getIdx(lines2[0])
	N = len(grid1)
	if grid1[move[0]][move[1]] == '*':
		print("Invalid move on star mark.")
		return
	dfs(grid1, move[0], move[1], N, grid1[move[0]][move[1]])

	grid2 = []
	for i in range(1, len(lines2)):
		line = list(lines2[i])
		grid2.append(line)

	for c in range(N):
		col1 = [row[c] for row in grid1]
		col1 = [e for e in col1 if e != '*']
		col2 = [row[c] for row in grid2]
		col2 = [e for e in col2 if e != '*']
		if col1 != col2:
			print("-- Wrong result from given move.")
			return
	print("-- Correct result from given move, Congrat!")

print("---- Run 10 testcases on 3 agent ----")
print("Random Agent: ")
for i in range(1, 11):
	s = time.time()
	agent = RandomAgent("testcases/input"+str(i)+".txt")
	move = agent.predict_best_move()
	point = agent.move(agent.grid, move[0], move[1])
	agent.write_grid("testcases/output"+str(i)+"_random.txt", move[0], move[1])
	e = time.time() - s
	print("Test case " + str(i))
	print("- Process time: "+str(e)+" secs")
	verify(i, "testcases/input"+str(i)+".txt", "testcases/output"+str(i)+"_random.txt")
print()

print("Minimax Agent: ")
for i in range(1, 11):
	if i == 6 or i == 7 or i == 9:
		continue;
	s = time.time()
	agent = MinimaxAgent("testcases/input"+str(i)+".txt")
	move = agent.predict_best_move(3)
	agent.write_next_grid("testcases/output"+str(i)+"_minimax.txt")
	e = time.time() - s
	print("Test case " + str(i))
	print("- Process time: "+str(e)+" secs")
	print("- Searched node: " + str(agent.searched_node))
	print("- Average time per node: "+str(e/agent.searched_node))
	verify(i, "testcases/input"+str(i)+".txt", "testcases/output"+str(i)+"_minimax.txt")
print()

print("Minimax with αβ pruning Agent: ")
for i in range(1, 11):
	s = time.time()
	agent = MinimaxAgentPruning("testcases/input"+str(i)+".txt")
	move = agent.predict_best_move(3)
	agent.write_next_grid("testcases/output"+str(i)+"_minimax_ab.txt")
	e = time.time() - s
	print("Test case " + str(i))
	print("- Process time: "+str(e)+" secs")
	print("- Searched node: " + str(agent.searched_node))
	print("- Average time per node: "+str(e/agent.searched_node))
	verify(i, "testcases/input"+str(i)+".txt", "testcases/output"+str(i)+"_minimax_ab.txt")
print()


