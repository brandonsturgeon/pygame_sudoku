from os import listdir
from random import choice

class Puzzle():

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def get_puzzle(self):
        puzzle_dir = "puzzles/{}/".format(self.difficulty)

        files = listdir(puzzle_dir)
        to_open = choice(files)
        #to_open = "TEXT.txt"
        print to_open

        with open(puzzle_dir+to_open, "rb") as puzzle_file:
            puzzle_line = puzzle_file.read()

        # This is super weird. Seriously good luck decyphering this.
        # It took me all morning and I have pages scribbled on like a madman.
        # I'll need to make a video to explain this shiz.

        # Essentially the solved sudoku data I get is in data streaming
        # from top left to bottom right, but we make a single block and then
        # make the tiles inside that block. It make sense, seriously. If I could show you you'd get it.

        newstr = ""

        # Top row
        for i in range(0, 7, 3):
            print "--"
            for b in range(i, i+19, 9):
                newstr += puzzle_line[b:b+3]

        # Middle row
        for i in range(27, 34, 3):
            print "--"
            for b in range(i, i+19, 9):
                newstr += puzzle_line[b:b+3]

        # Bottom row
        for i in range(54, 61, 3):
            print "--"
            for b in range(i, i+19, 9):
                newstr += puzzle_line[b:b+3]

        return newstr
