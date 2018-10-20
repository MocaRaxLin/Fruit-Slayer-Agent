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

		branches = self.get_branches_rc(root.grid)

		for rc in branches:
			child_grid = [x[:] for x in root.grid] # child_grid = deepcopy(root.grid)
			points = self.move(child_grid, rc[0], rc[1])
			child = None
			if root.find_max:
				child = AlphaBetaState(child_grid, rc, root.points + points, False, root.depth-1, root.alpha, root.beta)
			else:
				child = AlphaBetaState(child_grid, rc, root.points - points, True, root.depth-1, root.alpha, root.beta)
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
		