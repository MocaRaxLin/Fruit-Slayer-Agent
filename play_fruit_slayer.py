import os
import sys
import re
import random
import copy

def grid_generator():
	N = int(random.random()*26) + 1
	P = int(random.random()*9) + 1
	grid = [[chr(ord('0') + int(random.random()*P)) for i in range(N)] for j in range(N)]
	return [N, P, grid]

def write_input(N:int, P:int, remaining_time:float, grid):
	file = open("input.txt", 'w')
	file.write(str(N) + '\n')
	file.write(str(P) + '\n')
	file.write(str(remaining_time) + '\n')
	for row in grid:
		line = ''.join(row) + '\n'
		file.write(line)
	file.close()
	return

def get_user_time() -> float:
	file = open("time.txt", mode='r')
	lines = list(file.readlines())
	file.close()
	user_time = lines[2].split() # split by whitespace like \t, \s, \n
	time = re.compile("[s|m]").split(user_time[1])
	# print(time)
	sec = float(time[0])*60 + float(time[1])
	return sec

def read_output(file_name:str):
	file = open(file_name, mode='r')
	lines = list(file.readlines())
	file.close()
	move = lines[0]
	new_grid = []
	for i in range(1, len(lines)):
		line = list(lines[i])
		line.pop()
		new_grid.append(line)
	return [move, new_grid]

def dfs(grid, r, c, N, p) -> int:
	if r == -1 or c == -1 or r == N or c == N or grid[r][c] != p:
		return 0
	grid[r][c] = '*'
	ret = 1
	ret += dfs(grid, r-1, c, N, p)
	ret += dfs(grid, r+1, c, N, p)
	ret += dfs(grid, r, c-1, N, p)
	ret += dfs(grid, r, c+1, N, p)
	return ret

def getIdx(move:str):
	c = ord(move[0]) - ord('A')
	r = int(move[1:]) - 1
	return [r, c]

def verified(grid, output_data) -> bool:
	move = getIdx(output_data[0])
	N = len(grid)
	if grid[move[0]][move[1]] == '*':
		print("Invalid move on star mark.")
		return False

	points = dfs(grid, move[0], move[1], N, grid[move[0]][move[1]])
	output_data.append(points*points)
	
	grid2 = output_data[1]
	# print(grid)
	# print(grid2)

	for c in range(N):
		col1 = [row[c] for row in grid]
		col1 = [e for e in col1 if e != '*']
		col2 = [row[c] for row in grid2]
		col2 = [e for e in col2 if e != '*']
		if col1 != col2:
			print("-- Wrong result from given move.")
			return False
	return True

def is_empty(grid) -> bool:
	N = len(grid)
	for r in range(N):
		for c in range(N):
			if grid[r][c] != '*':
				return False
	return True
# player A against player B
# python3 play_fruit_slayer.py random minimax
# python3 play_fruit_slayer.py minimax random

# python3 play_fruit_slayer.py random minimax_ab
# python3 play_fruit_slayer.py minmax_ab random

# python3 play_fruit_slayer.py minimax minimax_ab
# python3 play_fruit_slayer.py minmax_ab minimax

# print('Number of arguments: ' + str(len(sys.argv)) + ' arguments.')
print('Argument List: ' + str(sys.argv))

scriptA = sys.argv[1] + "_agent.py"
scriptB = sys.argv[2] + "_agent.py"

print("-----------Fruit Slayer-----------")
print("Player A: " + scriptA)
print("Player B: " + scriptB)

no_competition = 100
runs = 0
a_win = 0
b_win = 0
no_tie = 0

random.seed(42)

while runs < no_competition:

	score_A = 0
	score_B = 0

	turn = 0 # 0 -> A, 1 -> B
	init_board = grid_generator()
	N = init_board[0]
	P = init_board[1]
	for i in range(2):
		turn = i # A go first, then B go first
		time_A = 300.0
		time_B = 300.0
		grid = copy.deepcopy(init_board[2])
		print("Turn "+str(i+1) + ", Init board:")
		for row in grid:
			print(row)
		print()
		while time_A > 0 and time_B > 0:
			if turn == 0:
				write_input(N, P, time_A, grid)
				output = os.popen("{ time python3 "+scriptA+"; } 2> time.txt").read()
				time_A -= get_user_time()
				if time_A < 0:
					break
				output_data = read_output("output.txt")
				if not verified(grid, output_data): # move grid points
					time_A = -1
					break;
				score_A += output_data[2]
				print("score_A: " + str(score_A))
				print("remaining_time of A: " + str(time_A))
				grid = output_data[1]
				turn = 1

			elif turn == 1:
				write_input(N, P, time_B, grid)
				output = os.popen("{ time python3 "+scriptB+"; } 2> time.txt").read()
				time_B -= get_user_time()
				if time_B < 0:
					break
				output_data = read_output("output.txt")
				if not verified(grid, output_data):
					time_B = -1
					break;
				score_B += output_data[2]
				print("score_B: " + str(score_B))
				print("remaining_time of B: " + str(time_B))
				grid = output_data[1]
				turn = 0

			print("Current board:")
			for row in grid:
				print(row)
			print()
			if is_empty(grid):
				break

	print("Result: ")
	if time_A < 0:
		print(scriptB+" wins!")
		b_win += 1
	elif time_B < 0:
		print(scriptA+" wins!")
		a_win += 1
	elif score_A > score_B:
		print(scriptA+" wins!")
		a_win += 1
	elif score_A < score_B:
		print(scriptB+" wins!")
		b_win += 1
	else:
		print(scriptA+" ties with "+scriptB+".")
		no_tie += 1

	print(scriptA + ", Score_A: "+ str(score_A) + ", remaining time: " + str(time_A))
	print(scriptB + ", Score_B: "+ str(score_B) + ", remaining time: " + str(time_B))
	runs += 1

print(scriptA + " wins " + str(a_win/no_competition*100) + " percent of games")
print(scriptB + " wins " + str(b_win/no_competition*100) + " percent of games")
print("Tie: " + str(no_tie/no_competition*100) + " percent of games")










