import sys
import os

# Maze file constants:
WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'

PLAYER = '@'  # (!) Try changing this to '+' or 'o'.
BLOCK = chr(9617)  # Character 9617 is '░'


def display_maze(maze, player_x, player_y):
    # Display the maze:
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == (player_x, player_y):
                print(PLAYER, end='')
            elif (x, y) == (exit_x, exit_y):
                print('X', end='')
            elif maze[(x, y)] == WALL:
                print(BLOCK, end='')
            else:
                print(maze[(x, y)], end='')
        print()  # Print a newline after printing the row.


def get_user_move():
    while True:
        print('                           W')
        print('Enter direction, or QUIT: ASD')
        move = input('> ').upper()

        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if move not in ['W', 'A', 'S', 'D']:
            print('Invalid direction. Enter one of W, A, S, or D.')
        else:
            return move


def can_move(maze, x, y, direction):
    if direction == 'W':
        return maze[(x, y - 1)] == EMPTY
    elif direction == 'S':
        return maze[(x, y + 1)] == EMPTY
    elif direction == 'A':
        return maze[(x - 1, y)] == EMPTY
    elif direction == 'D':
        return maze[(x + 1, y)] == EMPTY


def move_player(maze, player_x, player_y, move):
    while True:
        if move == 'W':
            player_y -= 1
        elif move == 'S':
            player_y += 1
        elif move == 'A':
            player_x -= 1
        elif move == 'D':
            player_x += 1

        if (player_x, player_y) == (exit_x, exit_y):
            return True, player_x, player_y

        if maze[(player_x, player_y)] == WALL:
            break  # Break if we've hit a wall.
        if (
            maze[(player_x - 1, player_y)] == EMPTY
            or maze[(player_x + 1, player_y)] == EMPTY
            or maze[(player_x, player_y - 1)] == EMPTY
            or maze[(player_x, player_y + 1)] == EMPTY
        ):
            break  # Break if we've reached a branch point.

    return False, player_x, player_y


print('Maze Runner 2D')

# Get the maze file's filename from the user:
while True:
    print('Enter the filename of the maze (or LIST or QUIT):')
    filename = input('> ')

    # List all the maze files in the current folder:
    if filename.upper() == 'LIST':
        print('Maze files found in', os.getcwd())
        for file_in_current_folder in os.listdir():
            if file_in_current_folder.startswith('maze') and file_in_current_folder.endswith('.txt'):
                print('  ', file_in_current_folder)
        continue

    if filename.upper() == 'QUIT':
        sys.exit()

    if os.path.exists(filename):
        break
    print('There is no file named', filename)

# Load the maze from a file:
maze_file = open(filename)
maze = {}
lines = maze_file.readlines()
player_x = None
player_y = None
exit_x = None
exit_y = None
y = 0

for line in lines:
    WIDTH = len(line.rstrip())
    for x, character in enumerate(line.rstrip()):
        assert character in (
            WALL, EMPTY, START, EXIT), f'Invalid character at column {x + 1}, line {y + 1}'
        if character in (WALL, EMPTY):
            maze[(x, y)] = character
        elif character == START:
            player_x, player_y = x, y
            maze[(x, y)] = EMPTY
        elif character == EXIT:
            exit_x, exit_y = x, y
            maze[(x, y)] = EMPTY
    y += 1
HEIGHT = y

assert player_x is not None and player_y is not None, 'No start in maze file.'
assert exit_x is not None and exit_y is not None, 'No exit in maze file.'

while True:  # Main game loop.
    display_maze(maze, player_x, player_y)
    move = get_user_move()
    success, player_x, player_y = move_player(maze, player_x, player_y, move)

    if success:
        display_maze(maze, player_x, player_y)
        print('You have reached the exit! Good job!')
        print('Thanks for playing!')
        sys.exit()
