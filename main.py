# Sudoku in Pygame

import pygame
import random

from lib.gen_puzzle import Puzzle

# COLORS #

# Primary
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Others
LIGHT_BLUE = (135, 206, 250)
GRAY = (175, 175, 175)
YELLOW = (255, 255, 0)

# Shades
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)




TILE_WIDTH = 90
TILE_SIZE = (TILE_WIDTH, TILE_WIDTH)

BLOCK_WIDTH = 274
BLOCK_SIZE = (BLOCK_WIDTH, BLOCK_WIDTH)

# Init font for global use
pygame.font.init()
FONT = pygame.font.Font(None, 104)
BOLD_FONT = pygame.font.Font(None, 104)
BOLD_FONT.set_bold(True)

class Block():

    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(self.pos, BLOCK_SIZE)

        self.surface = pygame.Surface(BLOCK_SIZE).convert()
        self.surface.fill(BLACK)

        self.tiles = []


class Tile():

    def __init__(self, block, pos, number, is_hint=False):
        self.block = block
        self.pos = pos

        # Actual answer
        self.number = number

        # Current provided answer
        self.entered_number = ""

        # If this tile was given to the player at the start
        self.is_hint = is_hint

        # Calculate global rectangle pos
        block_x_pos = self.block.rect.x
        block_y_pos = self.block.rect.y
        rect_pos_x = block_x_pos + self.pos[0]
        rect_pos_y = block_y_pos + self.pos[1]
        rect_pos = (rect_pos_x,
                    rect_pos_y)

        print "Tile created at: {}".format(rect_pos)
        self.rect = pygame.Rect(rect_pos, TILE_SIZE)

        self.surface = pygame.Surface(TILE_SIZE).convert()

        self.surface.fill(WHITE)

        if self.is_hint is True:
            self.draw_number(entry_text=self.number)
        else:
            self.draw_number()

    # This will draw self.entered_number unless entry_text is passed
    # Entry text is passed when a user selects this tile and types
    def draw_number(self, entry_text=None):

        # Render entry text if given, otherwise render the current entered number
        if entry_text is None:
            number_surface = FONT.render(str(self.entered_number), 1, BLACK)
        else:
            number_surface = FONT.render(str(entry_text), 1, BLACK)

        surface_center_x = self.surface.get_width()/2
        surface_center_y = self.surface.get_height()/2

        number_place_x = surface_center_x - number_surface.get_width()/2
        number_place_y = surface_center_y - number_surface.get_height()/2
        number_place = (number_place_x,
                        number_place_y)
        self.surface.blit(number_surface, number_place)


    def set_as_hint(self):
        self.entered_number = self.number
        self.draw_number(entry_text=self.number)
        self.is_hint = True



class Game():

    def __init__(self):

        # Boring pygame init stuff #
        pygame.init()
        self.clock = pygame.time.Clock()

        self.nav_height = 50

        # Game Width
        self.GW = 843
        # Game Height
        self.GH = 843
        # Tuple of game size
        self.GS = (self.GW, self.GH)

        flags = pygame.DOUBLEBUF
        self.game_window = pygame.display.set_mode(self.GS, flags)

        game_surface_size = (self.GW, self.GH)
        self.game_surface = pygame.Surface(game_surface_size).convert()

        nav_surface_size = (self.GW, self.nav_height)
        self.nav_surface = pygame.Surface(nav_surface_size).convert()
        self.nav_surface.fill(GRAY)

        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pos = (self.mouse_x,
                          self.mouse_y)


        # Fun Vars #

        self.blocks = []
        self.tiles = []

        self.tile_spacer = 2
        self.block_spacer = 5

        self.selected_tile = None
        # Text that has been entered
        self.entry_text = ""

        #self.valid_keys = ("K_0", "K_1", "K_2", "K_3", "K_4",
        #                   "K_5", "K_6", "K_7", "K_8", "K_9")
        self.number_keys = ("1","2","3","4","5","6","7","8","9")

        self.difficulty = "easy" # easy | medium | hard

        self.playing = True

        self.generate_board()
        self.main()


    def main(self):
        # TODO: refine this list
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN,
                                  pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN])
        while self.playing:

            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.playing = False
                    return

                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = pygame.mouse.get_pos()

                    # TODO: remove this if not needed
                    self.mouse_x, self.mouse_y = self.mouse_pos

                # TODO: see if we can use the pos attribute of MBdown
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # If there's one selected
                    # TODO: make this only happen if you clicked not on selected_tile
                    if self.selected_tile is not None:
                        self.unselect_tile()

                    # Nothing selected
                    else:
                        # See if it collided with anything
                        tile_rects = [x.rect for x in self.tiles]
                        cursor_rect = pygame.Rect(self.mouse_pos,(1,1))

                        collide_index = cursor_rect.collidelist(tile_rects)

                        # If it's colliding with something and it's a hint
                        if collide_index != -1:
                            if self.tiles[collide_index].is_hint is False:
                                self.selected_tile = self.tiles[collide_index]
                                self.selected_tile.surface.fill(LIGHT_BLUE)
                                self.entry_text = self.selected_tile.entered_number

                                if self.selected_tile.entered_number != "":
                                    self.highlight_tiles(self.selected_tile.entered_number)


                # TODO make long things like this a function
                elif event.type == pygame.KEYDOWN:
                    key = event.unicode

                    # If we're entering text:
                    if self.selected_tile is not None:

                        # If it's a number and entry text is empty, add it
                        if key in self.number_keys:
                            if self.entry_text == "":
                                self.entry_text = key

                        # If it's a backspace, reset entry text
                        elif keys[pygame.K_BACKSPACE]:
                            self.entry_text = ""

                        # If return is hit, submit the text
                        elif keys[pygame.K_RETURN]:
                            self.unselect_tile()

                    print "Entry Text: {}".format(self.entry_text)



            self.game_surface.fill(BLACK)
            for block in self.blocks:

                block.surface.fill(BLACK)
                # draw tiles to block surface
                for tile in block.tiles:
                    block.surface.blit(tile.surface, tile.pos)
                self.game_surface.blit(block.surface, block.pos)

            if self.selected_tile is not None:
                self.selected_tile.surface.fill(LIGHT_BLUE)
                self.selected_tile.draw_number(entry_text=self.entry_text)


            self.game_window.fill(BLACK)
            self.game_window.blit(self.game_surface, (0,0))
            pygame.display.flip()


            self.clock.tick(60)

    def unselect_tile(self):
        self.selected_tile.entered_number = self.entry_text
        self.entry_text = ""

        fill_color = GRAY
        if self.selected_tile.entered_number == "":
            fill_color = WHITE
        else:
            if self.selected_tile.number == self.selected_tile.entered_number:
                fill_color = GREEN
            else:
                fill_color = RED

        self.selected_tile.surface.fill(fill_color)
        self.selected_tile.draw_number()
        self.selected_tile = None


    def highlight_tiles(self, number):
        if number is "":
            return False

        tiles = self.tiles[:]
        tiles.remove(self.selected_tile)
        # Loop through all tiles, ignore the selected tile
        for tile in tiles:
            # If it's a tile that is a hint, or has a number entered
            if tile.is_hint is True or tile.entered_number is not "":
                if tile.entered_number == number:
                    # We highlight it yellow
                    tile.surface.fill(YELLOW)
                    tile.draw_number()

    def generate_board(self):
        puzzle = Puzzle(self.difficulty).get_puzzle()

        x_pos = self.block_spacer
        y_pos = self.block_spacer
        for y in xrange(3):
            for x in xrange(3):
                newpos = (x_pos, y_pos)
                newblock = Block(newpos)
                print "---------------------------------------"
                print "Generating block at: {}".format(newpos)

                # Generating Tiles
                tile_grid_x = 0
                tile_grid_y = 0
                for tile_y in xrange(3):
                    for tile_x in xrange(3):
                        # Generate a new Tile,
                        # associate it with the new block
                        newpos = (tile_grid_x, tile_grid_y)

                        number = puzzle[len(self.tiles)]

                        newtile = Tile(block=newblock,
                                       pos=newpos,
                                       number=number)
                        print "Generating tile at: {} with number: {}".format(newpos, number)
                        newblock.tiles.append(newtile)
                        self.tiles.append(newtile)

                        tile_grid_x += (TILE_WIDTH + self.tile_spacer)
                    tile_grid_y += (TILE_WIDTH + self.tile_spacer)
                    tile_grid_x = 0


                self.blocks.append(newblock)
                x_pos += (BLOCK_WIDTH + self.block_spacer)
            y_pos += (BLOCK_WIDTH + self.block_spacer)
            x_pos = self.block_spacer

        # Hurray we made the blocks
        # Now we need to uncover some of them.

        #I also insist that the
        #average number of clues hangs around 27 and is never more than 30. Nikoli, the inventor
        #of the modern version of Sudoku states as part of his definition that the number of clues
        #should not exceed 32.
        #
        #On the subject of clues, it is possible to reduce the number of clues1
        #to 17 and still provide a
        #spectrum of difficulty. It is also quite interesting to note that not every number 1 to 9 needs to be
        #present on the board, but certainly at least 8 of those numbers do need to be. If there were only
        #seven, for example the numbers 3 to 9, then all the 1s and all the 2s could be swapped around
        # - http://www.sudokuwiki.org/sudoku_creation_and_grading.pdf

        hint_difficulties = {"easy": (25,30),
                             "medium": (20,25),
                             "hard": (17,20)}
        num_hints = random.randint(*hint_difficulties[self.difficulty])

        hint_tiles = []
        # Create a copy of the tiles list
        tiles_copy = self.tiles[:]

        # Guarantees that we don't select the same number twice
        for i in range(num_hints):
            random_choice = random.choice(tiles_copy)
            tiles_copy.remove(random_choice)
            hint_tiles.append(random_choice)

        # Set them as given (hints)
        for tile in hint_tiles:
            tile.set_as_hint()





if __name__ == "__main__":
    Game()
