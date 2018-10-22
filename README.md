# Fruit-Slayer-Agents

## Game Description
The Fruit Rage is a two player game in which each player tries to maximize his/her share from a batch of fruits randomly placed in a box. The box is divided into cells and each cell is either empty(\*) or filled with one fruit(0-8) of a specific type.

At the beginning of each game, all cells are filled with fruits. Players play in turn and can pick a cell of the box in their own turn and claim all fruit of the same type, in all cells that are connected to the selected cell through horizontal and vertical paths. For each selection or move the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move. Once an agent picks the fruits from the cells, their empty place will be filled with other fruits on top of them (which fall down due to gravity), if any. In this game, no fruit is added during game play. Hence, players play until all fruits have been claimed.

The scores for each turn will count like this:
eliminate x fruit -> get x^2 points. 
In the end, the player with higher score win.

In addition, we give each player 300 seconds for the entire game. The player used up the 300 seconds will lose too.

## Project Agents
We built 3 agents, they are
1. Random agent
2. Minimax agent with lookahead at most 3 level
3. Minimax agent with lookahead at most 3 level **plus αβ pruning**

You can run one of the following commands to give a shot.
The competition(gaming) environment was set up properly.

~~~~
python3 play_fruit_slayer.py random minimax
python3 play_fruit_slayer.py random minimax_ab
python3 play_fruit_slayer.py minimax minimax_ab
~~~~

In the most cases, the agents runs slow (expect random agent), because searching time complexity on this minimax tree grows exponentially high.

level 1 -> b branches, 
level 2 -> b^b branches, 
level 3 -> b^b^b branches, 
... and so on.

So, if you don't want to wait so long, you can resize the gaming board (grid) or set smaller number of fruit type. (default: N=26, P=10)


## Customized Agent Instructions
Also you can modify or create a better agent to compete with mine.
Here are the input and output set up.

Each agent takes "input.txt" as input file to predict the next best move from current given grid.

Input format:
- 1st line: N:int, the width and height of the square board (0 < n <= 26)
- 2nd line: P:int, the number of furit types (0 < P <= 9).
- 3rd line: T:float, remaining time to play (T > 0).
- Next N lines: the N-by-N given current grid containing \* as empty cell or 1 digit as a certain type of fruit.

input example:
~~~~
10
4
1.276
3102322310
0121232013
3021111113
0221031132
0230011012
0323321010
2003022012
2202200021
0130000020
2200022231
~~~~

Then after predict the best move the agent should produce "output.txt" as output file.

Outout format:
- 1st line: move:string, the position the agent takes fruits from. a letter A-Z represents column, a interger 1-26 represents which row.
- Next N lines: the N-by-N result grid after taking the move of the 1st line.

output example:
~~~~
G8
31******10
010*****13
3022322*13
0221232*32
0221111*12
0331031310
2020011012
2203321121
0103022120
2232222231
~~~~

Have fun on my gaming agent :)




