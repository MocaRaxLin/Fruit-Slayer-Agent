from agent import Agent
from typing import List
from copy import deepcopy


class State(object):
	def __init__(self, grid:List[List[chr]], lastMove:List[int], points:int, find_max:bool, depth:int):
		super(State, self).__init__()
		self.grid = grid
		self.lastMove = lastMove # root[-1,-1]
		self.points = points
		self.find_max = find_max # True max node, False min node
		self.depth = depth

		self.nextMove = [-1,-1] # leaf[-1,-1]
		self.children = []

		if self.find_max:
			self.minimax_value = 

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


	def predict_best_move(self, lookahead:int) -> List[int]:
		# Use minimax tree with depth limit to 3 to predict best move
		# find_max -> find_min -> find_max -> leaves
		# level 0  -> level 1  -> level 2  -> level 3
		# depth 3  -> depth 2  -> depth 1  -> depth 0
		# return [row, col] index we take from self.grid

		def dfs_check(grid:List[List[chr]], r:int, c:int, n:int, p:int, seen:List[List[bool]]):
			if r == -1 or c == -1 or r == n or c == n or seen[r][c] or grid[r][c] != p:
				return
			seen[r][c] = True
			dfs_check(grid, r-1, c, n, p, seen)
			dfs_check(grid, r+1, c, n, p, seen)
			dfs_check(grid, r, c-1, n, p, seen)
			dfs_check(grid, r, c+1, n, p, seen)

		def get_branches_rc(grid:List[List[chr]]) -> List[List[int]]:
			n = len(grid)
			seen = [[False for i in range(n)] for j in range(n)]
			pool_ret = []
			for r in range(n):
				for c in range(n):
					if not seen[r][c] and grid[r][c] != '*':
						pool_ret.append([r,c])
						dfs_check(grid, r, c, n, grid[r][c], seen)
			return pool_ret


		def build_minimax(root:State):
			if root.depth == 0:
				return
			branches = get_branches_rc(root.grid)

			for rc in branches:
				# child_grid = deepcopy(root.grid)
				child_grid = [x[:] for x in root.grid]
				points = self.move(child_grid, rc[0], rc[1])
				child = None
				if root.find_max:
					child = State(child_grid, rc, root.points + points, False, root.depth-1)
				else:
					child = State(child_grid, rc, root.points - points, True, root.depth-1)
				build_minimax(child)
				root.children.append(child)

		# grid:List[List[chr]], lastMove:List[int], points:int, find_max:bool, depth:int
		copyed_grid = [x[:] for x in self.grid]
		self.minimax_root = State(copyed_grid, [-1,-1], 0, True, lookahead)
		build_minimax(self.minimax_root)


		return [-1,-1]







