# Homework 01 - Game of life
#
# Your task is to implement part of the cell automata called
# Game of life. The automata is a 2D simulation where each cell
# on the grid is either dead or alive.
#
# State of each cell is updated in every iteration based state of neighbouring cells.
# Cell neighbours are cells that are horizontally, vertically, or diagonally adjacent.
#
# Rules for update are as follows:
#
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
#
# Our implementation will use coordinate system will use grid coordinates starting from (0, 0) - upper left corner.
# The first coordinate is row and second is column.
#
# Do not use wrap around (toroid) when reaching edge of the board.
#
# For more details about Game of Life, see Wikipedia - https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


def update(alive, size, iter_n):
    new_alive = set()
    for n in range(iter_n):
        if n > 0:
            alive = new_alive
            new_alive = set()
        for i in range(size[0]):
            for j in range(size[1]):
                if (i,j) in alive:
                    alive_count = 0
                    for p in range(-1,2,1):
                        for q in range(-1,2,1):
                            if (i + p, j + q) in alive and 0 <= i+p < size[0] and 0<= j + q < size[1] and (i + p != i or j + q != j):
                                alive_count += 1                   
                    if alive_count == 2 or alive_count == 3:  #rule for live cell applied                      
                        new_alive.add((i, j))
                else:
                    alive_dead_count = 0
                    for p in range(-1, 2, 1):
                        for q in range(-1, 2, 1):
                            if (i + p, j + q) in alive and 0 <= i + p < size[0] and 0 <= j + q < size[1] and (i + p != i or j + q != j):
                                alive_dead_count += 1
                    if  alive_dead_count == 3: # rule for dead cell applied
                        new_alive.add((i, j))
                       
    sorted(new_alive, key= lambda x: (x[0],x[1]))
    return new_alive

def draw(alive, size):
    """
    alive - set of cell coordinates marked as alive, can be empty
    size - size of simulation grid as  tuple - (

    output - string showing the board state with alive cells marked with X
    """
    # TODO: implement board drawing logic and return it as output
    # Don't call print in this method, just return board string as output.
    # Example of 3x3 board with 1 alive cell at coordinates (0, 2):
    # +---+
    # |  X|
    # |   |
    # |   |
    # +---+

    
    drawing = str()
    drawing += '+'
    for i in range(size[1]):
        drawing+='-'
    drawing+='+\n'
    for i in range(size[0]):
        for j in range(size[1]):
            if j == 0:
                drawing+='|'
            if (i,j) in alive:
                drawing+= 'X'
            else:
                drawing+=' '
            if j == size[1] - 1:
                drawing += '|\n'
    drawing+= '+'
    for i in range(size[1]):
        drawing+='-'
    drawing += '+'

    return drawing
   

