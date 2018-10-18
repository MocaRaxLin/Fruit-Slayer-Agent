from typing import List

class Agent:
	def __init__(self, file_name:str):
		self.grid = []
		self.N = -1
		self.type = -1
		self.time = -1
		self.load_data(file_name)

	def load_data(self, file_name):
		file = open(file_name, mode='r')
		self.N = int(file.readline())
		self.type = int(file.readline())
		self.time = float(file.readline())
		for i in range(self.N):
			line = file.readline()
			line = list(line)
			if len(line) > self.N:
				line.pop()
			self.grid.append(line)
		file.close()

	def print_info(self):
		print("types = " + str(self.type))
		print("time = " + str(self.time))
		for line in self.grid:
			print(line)
		print()

	def predict_best_move(self) -> str:
		pass

	def move(self, row:int, col:int) -> int:
		def dfs(grid, r, c, N, p, seen) -> int:
			if r == -1 or c == -1 or r == N or c == N:
				return 0
			if seen[r][c] or grid[r][c] == '*' or grid[r][c] != p:
				return 0
			seen[r][c] = True
			grid[r][c] = '*'
			point = 0
			point += dfs(grid, r-1, c, N, p, seen)
			point += dfs(grid, r+1, c, N, p, seen)
			point += dfs(grid, r, c-1, N, p, seen)
			point += dfs(grid, r, c+1, N, p, seen)
			return point + 1

		def drop(grid, c, N):
			bot = N - 1
			for r in reversed(range(N)):
				if grid[r][c] != '*':
					grid[bot][c] = grid[r][c]
					bot -= 1
			while bot >= 0:
				grid[bot][c] = '*'
				bot -= 1

		# take
		p = self.grid[row][col]
		seen = [[False for i in range(self.N)] for j in range(self.N)]
		ret = 0
		ret = dfs(self.grid, row, col, self.N, p, seen)

		# drop
		for c in range(self.N):
			drop(self.grid, c, self.N)

		return ret*ret

	def write_grid(self, file_name, r, c):
		file = open(file_name, 'w')
		take = chr(ord('A')+c+1) + str(r+1) + '\n'
		file.write(take)
		for row in self.grid:
			line = ''.join(row) + '\n'
			file.write(line)





