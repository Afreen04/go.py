#!/usr/bin/env python

import argparse
import sys
import numpy as numpy

from collections import deque

from go import Board, BoardError, View, clear, getch, Location


def main():
    # Get arguments
    """
    parser = argparse.ArgumentParser(description='Starts a game of go in the terminal.')
    parser.add_argument('-s', '--size', type=int, default=19, help='size of board')

    args = parser.parse_args()

    if args.size < 7 or args.size > 19:
        sys.stdout.write('Board size must be between 7 and 19!\n')
        sys.exit(0)
"""
    # Initialize board and view
    board = Board(7)
    view = View(board)
    err = None
    board_history = deque(maxlen=8)

    # User actions
    def move():
        """
        Makes a move at the current position of the cursor for the current
        turn.
        """
        print("Getting our input for x and y")
        x = input("Input x:")
        y = input("Input y:")

        view.set_coordinates(x,y)
        
        board.move(*view.cursor)
        view.redraw()

        print("Board state")
        #print(*board._state) #This is list
        
        board_state =  []

        #Creating the board state

        for item in board._state[0]:
            row = []
            for elem in item:
                #print(type(elem))
                if elem == Location('empty'):
                    row.append(0)
                elif elem == Location('black'):
                    row.append(1)
                else:
                    row.append(2)
            
            board_state.append(row)

        board_history.append(board_state)

        print(board_state)
        ctr = 0
        for item in board_history:
            print(ctr,"  ",item)
            ctr = ctr + 1
        #print("\n".join(board_history))

    def undo():
        """
        Undoes the last move.
        """
        board.undo()
        view.redraw()

    def redo():
        """
        Redoes an undone move.
        """
        board.redo()
        view.redraw()

    def exit():
        """
        Exits the game.
        """
        sys.exit(0)

    # Action keymap
    KEYS = {
        'w': view.cursor_up,
        's': view.cursor_down,
        'a': view.cursor_left,
        'd': view.cursor_right,
        ' ': move,
        'u': undo,
        'r': redo,
        '\x1b': exit,
    }

    # Main loop
    while True:
        # Print board
        #clear()
        sys.stdout.write('{0}\n'.format(view))
        sys.stdout.write('Black: {black} <===> White: {white}\n'.format(**board.score))
        sys.stdout.write('{0}\'s move... '.format(board.turn))

        if err:
            sys.stdout.write('\n' + err + '\n')
            err = None

        # Get action key
       # c = getch()

        try:
            # Execute selected action
            #KEYS[c]()
            move()
        except BoardError as be:
            # Board error (move on top of other piece, suicidal move, etc.)
            print("Illegal Move")
            #err = be.message
        except KeyError:
            # Action not found, do nothing
            pass


if __name__ == '__main__':
    main()
