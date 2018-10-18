from agent import Agent
from typing import List

class MiniMaxAgent(Agent):
	def __init__(self, fileName):
		super(MiniMaxAgent, self).__init__(fileName)
	
	def predict_best_move(self) -> List[int]:
		# Use minimax tree with depth limit to 3 to predict best move