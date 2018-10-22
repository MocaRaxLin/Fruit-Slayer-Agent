import random

from agent import Agent
from typing import List
		
class RandomAgent(Agent):
	def __init__(self, fileName:str):
		super(RandomAgent, self).__init__(fileName)
	
	def predict_best_move(self) -> List[int]:
		# collect valid [r, c]
		pool = []
		for r in range(self.N):
			for c in range(self.N):
				if self.grid[r][c] != '*':
					pool.append([r,c])
		# random pick one
		r = random.random()*len(pool)
		idx = int(r)
		return pool[idx]


if __name__ == '__main__':
	agent = RandomAgent("input.txt")
	move = agent.predict_best_move()
	agent.move(agent.grid, move[0], move[1])
	agent.write_grid("output.txt", move[0], move[1])
