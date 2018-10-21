
from agent import Agent

agent = Agent("input6.txt")
print("---- load_data test ------")
agent.print_info()

print("---- move test ------")
points = agent.move(agent.grid, 4, 7)
print("points = " + str(points))
agent.print_info()

print("---- write_grid test ------")
agent.write_grid("test_output6.txt", 4, 7)
print("see test_output6.txt in folder!")