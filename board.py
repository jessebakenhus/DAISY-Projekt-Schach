from operator import is_
import os
import numpy as np
from uuid import uuid4
from pieces import Pawn, Rook, Bishop, Queen, King, Knight
from util import (
    map_piece_to_character,
    InvalidColumnException,
    InvalidRowException,
)


class BoardBase:
    """
    Base Class for the Chess Board.
    You are free to look around the members of this class and their implementation, however you will not need to change
    anything in this class for any of the tasks.
    """

    def __init__(self):
        """Constructor.
        Start with empty cells
        """
        self.cells = [[None for _ in range(8)] for _ in range(8)]
        self.check_cache = {}

    def __str__(self):
        """
        Returns a nice printable (on console) representation for the current board configuration.
        This is an extended form, meant for readability on console output.
        """
        return "\n".join(
            [
                " ".join([map_piece_to_character(cell) for cell in row])
                for row in reversed(self.cells)
            ]
        )

    def hash(self):
        """
        Returns a unique hash (string) representation for the current board configuration.
        This is short form, not meant for readability.
        """
        return "".join(
            [
                "".join([map_piece_to_character(cell) for cell in row])
                for row in reversed(self.cells)
            ]
        )
    
    def save_to_disk(self, fname = None):
        """
        Saves current board configuration to disk.

        :param name: Filename to use. If None is provided, a unique one will be generated
        """
        if fname is None:
            fname = str(uuid4())

        if '.' not in fname:
            fname += ".board"

        with open(fname, "wt") as f:
            f.write(str(self))

    def clear_board(self):
        """
        Clears to board, deleting all pieces currently placed on it
        """
        self.cells = [[None for _ in range(8)] for _ in range(8)]


    def load_from_memory(self, configString):
        """
        Read previously stored configuration from a memory string

        :param name: Filename to use. 
        """       
        self.cells = [[None for _ in range(8)] for _ in range(8)]

        for row, line in enumerate(configString.split("\n")):
              line = line.strip()
              for col, pieceCode in enumerate(line.split(' ')):
                if pieceCode == '.':
                    continue
                
                if pieceCode.isupper():
                    white = True
                else:
                    white = False

                pieceCode = pieceCode.upper()

                if pieceCode == "P":
                    piece = Pawn(self, white)
                if pieceCode == "K":
                    piece = King(self, white)
                if pieceCode == "Q":
                    piece = Queen(self, white)
                if pieceCode == "N":
                    piece = Knight(self, white)
                if pieceCode == "B":
                    piece = Bishop(self, white)
                if pieceCode == "R":
                    piece = Rook(self, white)

                self.set_cell(np.array([7-row, col]), piece)

    def load_from_disk(self, fname):
        """
        Read previously stored configuration from disk

        :param name: Filename to use. 
        """       

        with open(fname, "rt") as f:
            self.load_from_memory(f.read())
            

    def is_king_check_cached(self, white):
        """
        Calls is_king_check for board configurations not yet known. Caches the result for later look-up.
        """
        # Calculate hash and see if current position is in the cache
        hash = self.hash() + "-w" if white else "-b"
        if hash in self.check_cache:
            return self.check_cache[hash]

        # No, so evaluate it
        value = self.is_king_check(white)

        # Cache it for later
        self.check_cache[hash] = value
        return value

    def get_cell(self, cell):
        """
        Retrieves the piece placed on the given cell or "None" if cell is invalid
        """
        # If the cell is not valid, there cannot be a piece on it
        if not self.is_valid_cell(cell):
            return None

        # Unpack coordinates
        row, col = cell

        # Return the piece on the cell
        return self.cells[row][col]

    def set_cell(self, cell, piece):
        """
        Places a piece on a given cell.
        """
        # Unpack coordinates
        row, col = cell

        # Check if they are valid, raise an Exception if not
        if row < 0 or row >= 8:
            raise InvalidRowException((row, col))

        if col < 0 or col >= 8:
            raise InvalidColumnException((row, col))

        # If there is a piece to place, there is maintenance stuff to do
        if piece is not None:
            # If the piece has a cell (so it was placed on the board already), set that cell to None
            if piece.cell is not None:
                self.set_cell(piece.cell, None)

            # Update the pieces cell
            piece.cell = np.array([row, col])

        # Update the cell on the board
        self.cells[row][col] = piece

    def reset(self):
        """
        Resets the board to its default (start) configuration
        """
        # Start with all empty cells
        self.cells = [[None for _ in range(8)] for _ in range(8)]

        # Pawns
        for col in range(8):
            self.set_cell(np.array([1, col]), Pawn(self, True))
            self.set_cell(np.array([6, col]), Pawn(self, False))

        # Rooks
        self.set_cell(np.array([0, 0]), Rook(self, True))
        self.set_cell(np.array([0, 7]), Rook(self, True))
        self.set_cell(np.array([7, 0]), Rook(self, False))
        self.set_cell(np.array([7, 7]), Rook(self, False))

        # Knights
        self.set_cell(np.array([0, 1]), Knight(self, True))
        self.set_cell(np.array([0, 6]), Knight(self, True))
        self.set_cell(np.array([7, 1]), Knight(self, False))
        self.set_cell(np.array([7, 6]), Knight(self, False))

        # Bishops
        self.set_cell(np.array([0, 2]), Bishop(self, True))
        self.set_cell(np.array([0, 5]), Bishop(self, True))
        self.set_cell(np.array([7, 2]), Bishop(self, False))
        self.set_cell(np.array([7, 5]), Bishop(self, False))

        # Queen
        self.set_cell(np.array([0, 3]), Queen(self, True))
        self.set_cell(np.array([7, 3]), Queen(self, False))

        # King
        self.set_cell(np.array([0, 4]), King(self, True))
        self.set_cell(np.array([7, 4]), King(self, False))

        #self.save_to_disk()


class Board(BoardBase):
    """
    Your implementation of the chess board. You will need to find implementations for all of these methods. 

    **HINT**: Read the documentation carefully. Also look at the parent class (BoardBase) for further reference and example implementations. 
    """

    def __init__(self):
        """
        Constructor, currently does nothing but calling the super constructor. 

        """
        super().__init__()

    def iterate_cells_with_pieces(self, white):
        """
        **TODO**: Write a generator (using the yield keyword) that allows to iterate
        over all cells with a piece of given color.

        **HINT**: You need a double-nested loop,
        the first one iterates over all the rows, the second one iterates over each cell in the current row.
        If the cell has a piece (so it is not None) and the piece has the correct color, *yield* it

        :param white: True if WHITE pieces are to be iterated, False otherwise
        :type white: Boolean
        """
        for row in range(8):
            for col in range(8):

                piece = self.get_cell((row, col))

                if piece is not None and piece.white == white:
                    yield piece


    def find_king(self, white):
        """
        **TODO**: Find the king piece of given color and return that piece

        **HINT**: You can use the iterate_cells_with_pieces() Method to find all
        pieces of a given color

        :param white: True if WHITE pieces are to be iterated, False otherwise
        :type white: Boolean

        :return: The :py:class:'King': object of the given color or None if there is no King on the board.
        """
        for piece in self.iterate_cells_with_pieces(white):
            if isinstance(piece, King):
                return piece

        return None

    def is_king_check(self, white):
        """
        **TODO**: Evaluate if the king of given color is currently in check.
        A check is given if any opposing piece can beat the king in its next move.

        **HINT**: You can use the find_king() Method to find the king of the given color.
        Then use the iterate_cells_with_pieces Method to find all pieces of *opposing color* (negate the "white"-parameter)
        For each opposing piece, call the "get_reachable_cells()" method to get a list of all reachable cells.
        Iterate over each reachable cell and check if the kings cell is reachable. If yes, shortcut and return True right away.
        """
        # TODO: Implement

    def evaluate(self):
        """
        **TODO**: Evaluate the current board configuration into a numerical number.
        The higher the number, to more favorable for WHITE (note: This is always from whites perspective!) the current configuration is.


        **HINT**: Start with a score of zero.
        Use the iterate_cells_with_pieces Method to find all WHITE pieces and call their respective "evaluate" Method. Sum those scores up.
        Then use the iterate_cells_with_pieces Method to find all BLACK pieces, call their respective "evaluate" Method and substract that from the score.
        """
        # TODO: Implement
        score = 0.0
        return score

    def is_valid_cell(self, cell):
        """
        **TODO**: Check if the given cell coordinates are valid. A cell coordinate is valid if both
        row and coloumn are between 0 and 7 inclusively.

        **HINT**:
        Cell is a tuple (row, col) of row and column. Unpack the tuple and check both row and col for
        being within the allowed range (0 to 7 inclusively).
        Don´t forget to handle the special case of "cell" being None. Return False in that case
        """
        if cell == None:
            return False

        row, col = cell #Teilt cell (Tupel) in zwei variablen auf -> Position 1 und 2 vom Tupel

        return (row >= 0 and row <= 7) and (col >= 0 and col <= 7) #Prüft ob beide Position innerhalb von 0 und 7 liegen

    def cell_is_valid_and_empty(self, cell):
        """
        **TODO**: Check if the given cell is empty, meaning there is no piece placed on it.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it and return True if there is None
        """
        return self.is_valid_cell(cell) and self.get_cell(cell) == None

    def piece_can_enter_cell(self, piece, cell):
        """
        **TODO**: Check if the given piece can enter the given cell.
        Note: You don´t need to check movement rules for the individual piece here. You only need to answer the question
        whether the piece can be placed on the given cell or not.

        A piece can be placed on a cell if the cell is valid and either empty or an opposing piece is placed here.
        A cell cannot be entered if a piece of the same color is already in that cell.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it. If there is None, this cell can be entered
        If, however, there is another piece, it must be of opposing color. Check the other pieces "white" attribute and compare against
        the given piece "white" attribute.
        """
        if not self.is_valid_cell(cell):
            return False
        
        return (self.get_cell(cell) == None) or (self.get_cell(cell).is_white() != piece.is_white()) 
 

    def piece_can_hit_on_cell(self, piece, cell):
        """
        **TODO**: Check if the given piece can *hit* at the given cell.
        Note: You don´t need to check movement rules for the individual piece here. You only need to answer the question
        whether the piece can be placed on the given cell or not and hit an opposing piece.

        A piece can hit on a cell if the cell is valid and an opposing piece is placed here.
        A cell cannot be hit if the cell is empty or a piece of the same color is already in that cell.

        **HINT**:
        You can use the "is_valid_cell()" Method to verify the cell is valid in the first place.
        If so, use "get_cell()" to retrieve the piece placed on it. If there is None, this cell cannot be hit.
        If, however, there is another piece, it must be of opposing color. Check the other pieces "white" attribute and compare against
        the given piece "white" attribute.
        """
        if not self.is_valid_cell(cell=cell):
            return False
        
        if self.get_cell(cell=cell) == None:
            return False
        
        return self.get_cell(cell=cell).is_white() != piece.is_white()