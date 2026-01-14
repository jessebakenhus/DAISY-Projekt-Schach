import numpy as np
import sys 


class Piece:
    """
    Base class for pieces on the board. 
    
    A piece holds a reference to the board, its color and its currently located cell.
    In this class, you need to implement two methods, the "evaluate()" method and the "get_valid_cells()" method.
    """
    def __init__(self, board, white):
        """
        Constructor for a piece based on provided parameters

        :param board: Reference to the board this piece is placed on
        :type board: :ref:class:`board`
        """
        self.board = board
        self.white = white
        self.cell = None



    def is_white(self):
        """
        Returns whether this piece is white

        :return: True if the piece white, False otherwise
        """
        return self.white

    def can_enter_cell(self, cell):
        """
        Shortcut method to see if a cell on the board can be entered.
        Simply calls :py:meth:`piece_can_enter_cell <board.Board.piece_can_enter_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the provided cell can enter, False otherwise
        """
        return self.board.piece_can_enter_cell(self, cell)

    def can_hit_on_cell(self, cell):
        """
        Shortcut method to see if this piece can hit another piece on a cell.
        Simply calls :py:meth:`piece_can_hit_on_cell <board.Board.piece_can_hit_on_cell>` from the current board class.

        :param cell: The cell to check for. Must be a unpackable (row, col) type.
        :return: True if the piece can hit on the provided cell, False otherwise
        """
        return self.board.piece_can_hit_on_cell(self, cell)
    
    # damit funktion in dieser Klasse aufrufbar ist
    def get_value(self):
        pass

    def evaluate(self):
        """
        **TODO** Implement a meaningful numerical evaluation of this piece on the board.
        This evaluation happens independent of the color as later, values for white pieces will be added and values for black pieces will be substracted. 
        
        **HINT** Making this method *independent* of the pieces color is crucial to get a *symmetric* evaluation metric in the end.
         
        - The pure existance of this piece alone is worth some points. This will create an effect where the player with more pieces on the board will, in sum, get the most points assigned. 
        - Think of other criteria that would make this piece more valuable, e.g. movability or whether this piece can hit other pieces. Value them accordingly.
        
        :return: Return numerical score between -infinity and +infinity. Greater values indicate better evaluation result (more favorable).
        """
        # Wert der einzelnen Figuren
        piece_value = self.get_value()

        # mehr mögliche züge = mehr kontrolle übers spielfeld = more favorable
        
        anzahl_zuege = int(len(self.get_valid_cells()))
        
        # je mehr figuren die figur angreift, desto besser --> Bsp. Gabel Pferd

        bedrohungen = 0 
        schlagb_figuren = 0

        for foreign_piece in self.board.iterate_cells_with_pieces(not self.is_white()):

            foreign_cell = foreign_piece.cell

            #Figur vom Gegner wird abgefragt
            piece = self.board.get_cell(foreign_cell)
            # Anzahl an Figuren die uns schlagen können

            for cell in piece.get_valid_cells():
                if np.array_equal(self.cell, cell):
                    bedrohungen += 1

            # Anzahl an Figuren die wir schlagen können
            for cell in piece.get_valid_cells():
                if np.array_equal(foreign_cell, cell):
                    schlagb_figuren += 1


        # Wenn Anzahl an Bedrohungen kleiner gleich Anzahl an gedeckten Figuren (nicht implementiert), dann ist Position mehr Wert

        def berechne_anzahl_gedeckt():
            anzahl = 0
            
            posi = self.cell
            
            self.board.set_cell(posi, None)
            
            pieces = self.board.iterate_cells_with_pieces(self.is_white())
            
            for piece in pieces:
                for cell in piece.get_valid_cells():
                    if np.array_equal(cell, posi):
                        anzahl += 1
            
            self.board.set_cell(posi, self)

            return anzahl
            
        score = 0

        score += piece_value

        sicherheit = bedrohungen - berechne_anzahl_gedeckt()
        if sicherheit > 0:
            score -= piece_value * sicherheit
        else:
            score += piece_value * abs(sicherheit) * 0.3
        

        score += schlagb_figuren

        score += 0.1 * anzahl_zuege

        return score
        
        


            
            
           
                         
    
        
    



    # wenn gegnerische figuren die eigene schlagen könnten --> für jede figur 2 punkte abzug

        # anhand der kriterien die stellung bewerten
        # verhältnis finden zwischen kriterien (z.b. zählt die anzahl an figuren die 
        # geschlagen werden können mehr als nur die möglichen felder
        # wo die figur hinziehen kann )
        # beispiel:

        #points += (num_capturable_pieces * 2) + num_valid_moves
        


    def get_valid_cells(self):
        """
        **TODO** Return a list of **valid** cells this piece can move into. 
        
        A cell is valid if 
          a) it is **reachable**. That is what the :py:meth:`get_reachable_cells` method is for and
          b) after a move into this cell the own king is not (or no longer) in check.

        **HINT**: Use the :py:meth:`get_reachable_cells` method of this piece to receive a list of reachable cells.
        Iterate through all of them and temporarily place the piece on this cell. Then check whether your own King (same color)
        is in check. Use the :py:meth:`is_king_check_cached` method to test for checks. If there is no check after this move, add
        this cell to the list of valid cells. After every move, restore the original board configuration. 
        
        To temporarily move a piece into a new cell, first store its old position (self.cell) in a local variable. 
        The target cell might have another piece already placed on it. 
        Use :py:meth:`get_cell <board.BoardBase.get_cell>` to retrieve that piece (or None if there was none) and store it as well. 
        Then call :py:meth:`set_cell <board.BoardBase.set_cell>` to place this piece on the target cell and test for any checks given. 
        After this, restore the original configuration by placing this piece back into its old position (call :py:meth:`set_cell <board.BoardBase.set_cell>` again)
        and place the previous piece also back into its cell. 
        
        :return: Return True 
        """

        possible_moves = self.get_reachable_cells()

        valid_cells = []

        for move in possible_moves:

            origin_cell = self.cell # Speichern der ursprünglichen position
            possible_piece = self.board.get_cell(move) #get_cell gibt nicht position, sondern das piece auf der posi wieder

            self.board.set_cell(move, self) # simulieren der züge (temporär)

            if not self.board.is_king_check(self.is_white()):  # schach prüfung
                valid_cells.append(self.cell)

            self.board.set_cell(origin_cell, self)   # zurückstellen der figuren
            self.board.set_cell(move, possible_piece)

        return valid_cells





class Pawn(Piece):  # Bauer
    def __init__(self, board, white):
        super().__init__(board, white)
    # teilt figur wert zu
    def get_value(self):
        return 1

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanik for `pawns <https://de.wikipedia.org/wiki/Bauer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Pawns can move only forward (towards the opposing army). Depening of whether this piece is black of white, this means pawn
        can move only to higher or lower rows. Normally a pawn can only move one cell forward as long as the target cell is not occupied by any other piece. 
        If the pawn is still on its starting row, it can also dash forward and move two pieces at once (as long as the path to that cell is not blocked).
        Pawns can only hit diagonally, meaning they can hit other pieces only the are one cell forward left or one cell forward right from them. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the pawn movability mechanics. 

        **NOTE**: For all you deep chess experts: Hitting `en passant <https://de.wikipedia.org/wiki/En_passant>`_ does not need to be implemented.
        
        :return: A list of reachable cells this pawn could move into.
        """
        reachable_cells = []

        row, col = self.cell

        if self.is_white():

            if self.board.cell_is_valid_and_empty((row + 1, col)):
                reachable_cells.append((row + 1, col))

                if row == 1:
                    if self.board.cell_is_valid_and_empty((row + 2, col)):
                        reachable_cells.append((row + 2, col))

            # Diagonal schlagen
            if self.can_hit_on_cell((row + 1, col - 1)):
                reachable_cells.append((row + 1, col - 1))

            if self.can_hit_on_cell((row + 1, col + 1)):
                reachable_cells.append((row + 1, col + 1))

        else:

            if self.board.cell_is_valid_and_empty((row - 1, col)):
                reachable_cells.append((row - 1, col))

                # erster Schritt darf 2 nach vorne
                if row == 6:
                    if self.board.cell_is_valid_and_empty((row - 2, col)):
                        reachable_cells.append((row - 2, col))

            # Diagonal schlagen
            if self.can_hit_on_cell((row - 1, col - 1)):
                reachable_cells.append((row - 1, col - 1))

            if self.can_hit_on_cell((row - 1, col + 1)):
                reachable_cells.append((row - 1, col + 1))

        return reachable_cells
    



class Rook(Piece):  # Turm
    def __init__(self, board, white):
        super().__init__(board, white)
    # teilt figur wert zu
    def get_value(self):
        return 5

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `rooks <https://de.wikipedia.org/wiki/Turm_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Rooks can move only horizontally or vertically. They can move an arbitrary amount of cells until blocked by an own piece
        or an opposing piece (which they could hit and then being stopped).

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this rook could move into.
        """
        reachable_cells = []
        row, col = self.cell

        richtungen = [
            (-1, 0),  # vertikal nach oben
            (1, 0),  # vertikal nach unten
            (0, 1),  # horizontal nach rechts
            (0, -1)  # horizontal nach links
        ]

        # Durchlauf für jede Richtung und Diagonale
        for delta_row, delta_col in richtungen:

            # für die jeweilige Richtung und Diagonale das Spielfeld durch
            for i in range(1, 8):
                cell = (row + delta_row * i, col + delta_col * i)
                piece = self.board.get_cell(cell)

                if piece is None:
                    if self.can_enter_cell(cell):
                        reachable_cells.append(cell)
                else:
                    if self.can_hit_on_cell(cell):
                        reachable_cells.append(cell)
                    break

        return reachable_cells


class Knight(Piece):  # Springer
    def __init__(self, board, white):
        super().__init__(board, white)
    # teilt figur wert zu
    def get_value(self):
        return 3

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `knights <https://de.wikipedia.org/wiki/Springer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Knights can move in a special pattern. They can move two rows up or down and then one column left or right. Alternatively, they can
        move one row up or down and then two columns left or right. They are not blocked by pieces in between. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this knight could move into.
        """
        row, col = self.cell
        
        reachable_cell = [
            # 2 Reihen nach oben und rechts
            (row+2, col +1),
            # 2 Reihen anch oben und links
            (row+2, col -1),
            # eine Reihe nach oben und 2 rechts
            (row+1, col+2),
            # eine Reihe nach oben und 2 links
            (row+1, col-2),
            # eine Reihe nach unten und 2 rechts
            (row-1,col+2),
            # eine Reihe nach unten und 2 links
            (row-1,col-2),
            # 2 Reihen nach unten und rechts
            (row-2, col+1),
            # 2 Reihen nach unten und links
            (row-2, col-1)
        ]
        # gefilterte Liste reachable_cells wird zurückgegeben -> Figur kann auch schlagen 
        return [ cell for cell in reachable_cell if self.can_enter_cell(cell) or self.can_hit_on_cell(cell) ]


class Bishop(Piece):  # Läufer
    def __init__(self, board, white):
        super().__init__(board, white)
    # teilt figur wert zu
    def get_value(self):
        return 3

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for `bishop <https://de.wikipedia.org/wiki/L%C3%A4ufer_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Bishops can move diagonally an arbitrary amount of cells until blocked.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this bishop could move into.
        """
        reachable_cells = []
        row, col = self.cell

        richtungen = [
            (-1, 1),  # diagonal rechts oben
            (-1, -1),  # diagonal links oben
            (1, 1),  # diagonal rechts unten
            (1, -1),  # diagonal links unten
        ]

        # Durchlauf für jede Richtung und Diagonale
        for delta_row, delta_col in richtungen:

            # für die jeweilige Richtung und Diagonale das Spielfeld durch
            for i in range(1, 8):
                cell = (row + delta_row * i, col + delta_col * i)
                piece = self.board.get_cell(cell)

                if piece is None:
                    if self.can_enter_cell(cell):
                        reachable_cells.append(cell)
                else:
                    if self.can_hit_on_cell(cell):
                        reachable_cells.append(cell)
                    break

        return reachable_cells
        


class Queen(Piece):  # Königin
    def __init__(self, board, white):
        super().__init__(board, white)
    # teilt figur wert zu
    def get_value(self):
        return 9

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `queen <https://de.wikipedia.org/wiki/Dame_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Queens can move horizontally, vertically and diagonally an arbitrary amount of cells until blocked. They combine the movability
        of rooks and bishops. 

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this queen could move into.
        """

        reachable_cells = []
        row, col = self.cell

        richtungen = [
            (-1, 1),  # diagonal rechts oben
            (-1, -1),  # diagonal links oben
            (1, 1),  # diagonal rechts unten
            (1, -1),  # diagonal links unten
            (-1, 0),  # vertikal nach oben
            (1, 0),  # vertikal nach unten
            (0, 1),  # horizontal nach rechts
            (0, -1)  # horizontal nach links
        ]

        # Durchlauf für jede Richtung und Diagonale
        for delta_row, delta_col in richtungen:

            # für die jeweilige Richtung und Diagonale das Spielfeld durch
            for i in range(1, 8):
                cell = (row + delta_row * i, col + delta_col * i)
                piece = self.board.get_cell(cell)

                if piece is None:
                    if self.can_enter_cell(cell):
                        reachable_cells.append(cell)
                else:
                    if self.can_hit_on_cell(cell):
                        reachable_cells.append(cell)
                    break

        return reachable_cells

class King(Piece):  # König
    def __init__(self, board, white):
        super().__init__(board, white)

    # teilt figur wert zu
    def get_value(self):
        # sys.maxsize war zu viel: Subtraktion im Board funktioniert nicht mehr
        return 1e6

    def get_reachable_cells(self):
        """
        **TODO** Implement the movability mechanic for the `king <https://de.wikipedia.org/wiki/K%C3%B6nig_(Schach)>`_. 

        **NOTE**: Here you do not yet need to consider whether your own King would become checked after a move. This will be taken care of by
        the :py:meth:`is_king_check <board.Board.is_king_check>` and :py:meth:`get_valid_cells <pieces.Piece.get_valid_cells>` methods.

        **HINT**: Kings can move horizontally, vertically and diagonally but only one piece at a time.

        You can call :py:meth:`cell_is_valid_and_empty <board.Board.cell_is_valid_and_empty>`, 
        :py:meth:`can_hit_on_cell <pieces.Piece.can_hit_on_cell>` and :py:meth:`can_enter_cell <pieces.Piece.can_enter_cell>` 
        to check for necessary conditions to implement the rook movability mechanics. 

        :return: A list of reachable cells this king could move into.
        """

        row, col = self.cell 

        possible_reachable_cells = [
            (row - 1, col), # Links
            (row + 1, col), # Rechts
            (row, col + 1), # Oben
            (row, col - 1), # Unten
            (row - 1, col - 1), # Links Unten
            (row + 1, col - 1), # Rechts Unten
            (row - 1, col + 1), # Links Oben
            (row + 1, col + 1), # Rechts Oben
        ]

        reachable_cells = [ cell for cell in possible_reachable_cells if self.can_enter_cell(cell) ]

        return reachable_cells