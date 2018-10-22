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

		self.next_move = [-1,-1] # leaf[-1,-1], in alpha-beta[r, c, block]
		self.next_state = None
		if self.find_max:
			self.best = -float('inf')
		else:
			self.best = float('inf')

class MinimaxAgent(Agent):
	def __init__(self, file_name):
		super(MinimaxAgent, self).__init__(file_name)
		self.minimax_root = None
		self.searched_node = 0
	
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

	def get_branches(self, grid:List[List[chr]]) -> List[List[int]]:
		n = len(grid)
		seen = [[False for i in range(n)] for j in range(n)]
		pool_ret = []
		for r in range(n):
			for c in range(n):
				if not seen[r][c] and grid[r][c] != '*':
					child_grid = [x[:] for x in grid] # child_grid = deepcopy(grid)
					points = self.move_seen(child_grid, r, c, seen)
					pool_ret.append([r, c, points, child_grid])
		return pool_ret

	def build_minimax(self, root:State):
		if root.depth == 0:
			root.best = root.points
			return

		branches = self.get_branches(root.grid)
		b_size = len(branches)
		self.searched_node += b_size
		if b_size == 0:
			root.best = root.points
			return

		for data in branches:
			child = None
			rc = data[0:2]
			if root.find_max:
				# row = data[0], col = data[1], points = data[2], child_grid = data[3]
				child = State(data[3], rc, root.points + data[2], False, root.depth-1)
			else:
				child = State(data[3], rc, root.points - data[2], True, root.depth-1)
			self.build_minimax(child)

			if root.find_max:
				if root.best < child.best:
					root.next_move = rc
					root.next_state = child
					root.best = child.best
			else:
				if root.best > child.best:
					root.next_move = rc
					root.next_state = child
					root.best = child.best

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



def eval_func(N:int, P:int, T:float) -> int:
	if T < 100:
		return 1
	elif T < 200 or N > 10:
		return 2
	return 3

if __name__ == '__main__':
	agent = MinimaxAgent("input.txt")
	d = eval_func(agent.N, agent.type, agent.time)
	move = agent.predict_best_move(d)
	agent.write_next_grid("output.txt")





