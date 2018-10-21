from minimax_agent import State, MinimaxAgent
from typing import List

class AlphaBetaState(State):
	"""docstring for AlphaBetaState"""
	def __init__(self, grid:List[List[chr]], last_move:List[int], points:int, find_max:bool, depth:int, alpha:float, beta:float):
		super(AlphaBetaState, self).__init__(grid, last_move, points, find_max, depth)
		self.alpha = alpha
		self.beta = beta
		
class MinimaxAgentPruning(MinimaxAgent):
	def __init__(self, file_name):
		super(MinimaxAgentPruning, self).__init__(file_name)

	def dfs_check(self, grid:List[List[chr]], r:int, c:int, N:int, p:int, seen:List[List[chr]]) -> int:
		if r == -1 or c == -1 or r == N or c == N or seen[r][c] or grid[r][c] != p:
			return 0
		seen[r][c] = True
		ret = 1
		ret += self.dfs_check(grid, r-1, c, N, p, seen)
		ret += self.dfs_check(grid, r+1, c, N, p, seen)
		ret += self.dfs_check(grid, r, c-1, N, p, seen)
		ret += self.dfs_check(grid, r, c+1, N, p, seen)
		return ret

	def get_branches(self, grid:List[List[chr]], find_max:bool) -> List[List[int]]:
		n = len(grid)
		seen = [[False for i in range(n)] for j in range(n)]
		pool_ret = []
		for r in range(n):
			for c in range(n):
				if not seen[r][c] and grid[r][c] != '*':
					blocks = self.dfs_check(grid, r, c, n, grid[r][c], seen)
					pool_ret.append([r, c, blocks])
		# huristic improvement, try to get best move in early pruning
		pool_ret.sort(key=lambda x: x[2], reverse=find_max)
		return pool_ret

	def build_minimax_alpha_beta_pruning(self, root:AlphaBetaState):
		'''
		Pseudocode in general:
		function MINIMAX(node, depth, find_max, α, β):
			if depth == 0:
				return node.value
			if find_max:
				best_value = −∞
				for child in children:
					value = MINIMAX(child, depth-1, False, α, β)
					best_value = MAX(best_value, value)
					α = MAX(α, best_value)
					if α >= β:
						break
				return best_value
			else:
				best_value = +∞
				for child in children:
					value = MINIMAX(child, depth-1, True, α, β)
					best_value = MIN(best_value, value)
					β = MIN(β, best_value)
					if α >= β:
						break
				return best_value
		'''

		# return root point when we reach leaves
		if root.depth == 0:
			root.best = root.points
			return

		branches = self.get_branches(root.grid, root.find_max)
		b_size = len(branches)
		self.searched_node += b_size
		if b_size == 0:
			root.best = root.points
			return

		for data in branches:
			child_grid = [x[:] for x in root.grid] # child_grid = deepcopy(root.grid)
			rc = data[0:2]
			points = self.move(child_grid, rc[0], rc[1])
			child = None
			if root.find_max:
				child = AlphaBetaState(child_grid, rc, root.points + points, False, root.depth - 1, root.alpha, root.beta)
			else:
				child = AlphaBetaState(child_grid, rc, root.points - points, True, root.depth - 1, root.alpha, root.beta)
			self.build_minimax_alpha_beta_pruning(child)


			if root.find_max:
				if root.best < child.best:
					root.next_move = rc
					root.next_state = child
					root.best = child.best
				root.alpha = max(root.alpha, root.best)
			else:
				if root.best > child.best:
					root.next_move = rc
					root.next_state = child
					root.best = child.best
				root.beta = min(root.beta, root.best)

			root.children.append(child)
			if root.beta <= root.alpha:
				return

	def predict_best_move(self, lookahead:int) -> List[int]:

		# grid:List[List[chr]], lastMove:List[int], points:int, find_max:bool, depth:int
		copyed_grid = [x[:] for x in self.grid]
		self.minimax_root = AlphaBetaState(copyed_grid, [-1,-1], 0, True, lookahead, -float('inf'), float('inf'))
		self.build_minimax_alpha_beta_pruning(self.minimax_root)
		return self.minimax_root.next_move
		