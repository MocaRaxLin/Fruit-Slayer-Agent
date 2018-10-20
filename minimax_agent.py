from agent import Agent
from typing import List


class State(object):
	def __init__(self, grid:List[List[chr]], last_move:List[int], points:int, find_max:bool, depth:int):
		super(State, self).__init__()
		self.grid = grid
		self.last_move = last_move # root[-1,-1]
		self.points = points
		self.find_max = find_max # True max node, False min node
		self.depth = depth

		self.children = []

		self.next_move = [-1,-1] # leaf[-1,-1]
		self.next_state = None
		if self.find_max:
			self.minimax_value = -float('inf')
		else:
			self.minimax_value = float('inf')

class MinimaxAgent(Agent):
	def __init__(self, fileName):
		super(MinimaxAgent, self).__init__(fileName)
		self.minimax_root = None
	
	def print_minimax(self):
		def dfs_print_leaves(root:State) -> str:
			string = "{"
			if root.depth == 0:
				string += str(root.points)
			else:
				for child in root.children:
					string += dfs_print_leaves(child)
			string += "}"
			return string

		if self.minimax_root is None:
			print("self.minimax_root is None")
			return
		leaves_info = dfs_print_leaves(self.minimax_root)
		print(leaves_info)

	def dfs_check(self, grid:List[List[chr]], r:int, c:int, n:int, p:int, seen:List[List[bool]]):
		if r == -1 or c == -1 or r == n or c == n or seen[r][c] or grid[r][c] != p:
			return
		seen[r][c] = True
		self.dfs_check(grid, r-1, c, n, p, seen)
		self.dfs_check(grid, r+1, c, n, p, seen)
		self.dfs_check(grid, r, c-1, n, p, seen)
		self.dfs_check(grid, r, c+1, n, p, seen)

	def get_branches_rc(self, grid:List[List[chr]]) -> List[List[int]]:
		n = len(grid)
		seen = [[False for i in range(n)] for j in range(n)]
		pool_ret = []
		for r in range(n):
			for c in range(n):
				if not seen[r][c] and grid[r][c] != '*':
					pool_ret.append([r,c])
					self.dfs_check(grid, r, c, n, grid[r][c], seen)
		return pool_ret

	def build_minimax(self, root:State):
		if root.depth == 0:
			root.minimax_value = root.points
			return
		branches = self.get_branches_rc(root.grid)

		for rc in branches:
			child_grid = [x[:] for x in root.grid] # child_grid = deepcopy(root.grid)
			points = self.move(child_grid, rc[0], rc[1])
			child = None
			if root.find_max:
				child = State(child_grid, rc, root.points + points, False, root.depth-1)
			else:
				child = State(child_grid, rc, root.points - points, True, root.depth-1)
			self.build_minimax(child)


			if root.find_max:
				if root.minimax_value < child.minimax_value:
					root.next_move = rc
					root.next_state = child
					root.minimax_value = child.minimax_value
			else:
				if root.minimax_value > child.minimax_value:
					root.next_move = rc
					root.next_state = child
					root.minimax_value = child.minimax_value

			root.children.append(child)

	def predict_best_move(self, lookahead:int) -> List[int]:
		# Use minimax tree with depth limit to 3 to predict best move
		# find_max -> find_min -> find_max -> leaves
		# level 0  -> level 1  -> level 2  -> level 3
		# depth 3  -> depth 2  -> depth 1  -> depth 0
		# return [row, col] index we take from self.grid

		# grid:List[List[chr]], lastMove:List[int], points:int, find_max:bool, depth:int
		copyed_grid = [x[:] for x in self.grid]
		self.minimax_root = State(copyed_grid, [-1,-1], 0, True, lookahead)
		self.build_minimax(self.minimax_root)
		return self.minimax_root.next_move

	def write_next_grid(self, file_name):
		if self.minimax_root is None:
			print("run predict_best_move(lookahead:int) first to generate next_state")
			return
		self.grid = self.minimax_root.next_state.grid
		r = self.minimax_root.next_move[0]
		c = self.minimax_root.next_move[1]	
		self.write_grid(file_name, r, c)







