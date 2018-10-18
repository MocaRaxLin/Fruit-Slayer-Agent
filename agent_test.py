
from agent import Agent

# Comment @abstractmethod before you test

agent = Agent("test_input.txt")
print("---- load_data test ------")
agent.print_info()

print("---- move test ------")
points = agent.move(4, 7)
print("points = " + str(points)) # 14*14 = 196
agent.print_info()

print("---- write_grid test ------")
agent.write_grid("test_output.txt", 4, 7)
print("see test_output.txt in folder!") #I5