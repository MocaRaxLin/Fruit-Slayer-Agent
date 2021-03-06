from typing import List
		
class Agent:
	def __init__(self, file_name:str):
		self.grid = []
		self.N = -1
		self.type = -1
		self.time = -1
		self.load_data(file_name)

	def load_data(self, file_name:str):
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

	def print_grid(self, grid:List[List[chr]]):
		for line in grid:
			print(line)
		print()

	def predict_best_move(self) -> str:
		pass

	def move(self, grid:List[List[chr]], row:int, col:int) -> int:
		seen = [[False for i in range(len(grid))] for j in range(len(grid))]
		return self.move_seen(grid, row, col, seen)

	def move_seen(self, grid:List[List[chr]], row:int, col:int, seen:List[List[bool]]) -> int:
		# rerurn the points we get
		def dfs(grid:List[List[chr]], r:int, c:int, N:int, p:int, seen:List[List[bool]]) -> int:
			if r == -1 or c == -1 or r == N or c == N or seen[r][c] or grid[r][c] != p:
				return 0
				
			seen[r][c] = True
			grid[r][c] = '*'
			point = 1
			point += dfs(grid, r-1, c, N, p, seen)
			point += dfs(grid, r+1, c, N, p, seen)
			point += dfs(grid, r, c-1, N, p, seen)
			point += dfs(grid, r, c+1, N, p, seen)
			return point

		def drop(grid:List[List[chr]], c:int, N:int):
			bot = N - 1
			for r in reversed(range(N)):
				if grid[r][c] != '*':
					grid[bot][c] = grid[r][c]
					bot -= 1
			while bot >= 0:
				grid[bot][c] = '*'
				bot -= 1

		# take
		p = grid[row][col]
		N = len(grid)
		ret = 0
		ret = dfs(grid, row, col, N, p, seen) # seen from input parameter

		# drop
		for c in range(N):
			drop(grid, c, N)

		return ret*ret

	def write_grid(self, file_name:str, r:int, c:int):
		file = open(file_name, 'w')
		take = chr(ord('A')+c) + str(r+1) + '\n'
		file.write(take)
		for row in self.grid:
			line = ''.join(row) + '\n'
			file.write(line)
		file.close()





