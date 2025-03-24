import itertools
import random
from collections import deque


random.seed("1234")

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count>=len(self.cells):
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells: return

        self.cells.remove(cell)
        self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells: return

        self.cells.remove(cell)
        # self.count-=1

    def issubset(self, other):
        " return : (bool) is this a subset of other "
        return self.cells.issubset(other.cells)

    def __sub__(self, other):
        return self.cells - other.cells
    
    def __repr__(self):
        return f"{self.cells} = {self.count}"

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, game=None):
        self.game = game

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        # self.queue = deque()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        ptr = 0
        while ptr<len(self.knowledge):
            sentence = self.knowledge[ptr]
            sentence.mark_mine(cell)
            
            if sentence.known_safes():
                # if (3, 2) in sentence.cells: breakpoint()
                self.mark_sentence(self.knowledge.pop(ptr))
            else:
                ptr+=1

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        ptr = 0
        while ptr<len(self.knowledge):
            sentence = self.knowledge[ptr]
            sentence.mark_safe(cell)
            
            # adding safes can only lead to mines conclution
            if sentence.known_mines():
                # if (3, 2) in sentence.cells: breakpoint()
                self.mark_sentence(self.knowledge.pop(ptr))
            else:
                ptr+=1

    def valid_neibers(self, cell):
        i, j = cell
        neibers = []
        for i, j in [
            (i, j+1), (i, j-1),# left, right
            (i+1, j), (i-1, j),# up, down
            (i-1, j+1), (i-1, j-1),# uppner diogonals
            (i+1, j+1), (i+1, j-1)# loweer diogonals
        ]:
            if (
                i<0 or j<0 or i>=self.height or j>=self.width or
                (i, j) in self.moves_made or (i, j) in self.safes or (i, j) in self.mines
            ):
                continue

            # if (i, j) in self.mines:
            #     count-=1
            #     continue
        
            neibers.append((i, j))
        
        # return neibers, count
        return neibers

    def mark_sentence(self, sentence):
        # WARNING: make sure the sentence of cell is not in knowledge list

        for c in sentence.known_safes():
            if self.game.is_mine(c): breakpoint()
            self.mark_safe(c)
        for c in sentence.known_mines():
            self.mark_mine(c)
        
        # clearup checks
        
        # # reverse tracking
        # ptr = len(self.knowledge)-1
        # while ptr>=0:
        #     if not self.knowledge[ptr].cells:
        #         self.knowledge.pop(ptr)
        #     ptr-=1

        # # forward tracking
        # ptr = 0
        # while ptr<len(self.knowledge):
        #     if not self.knowledge[ptr].cells:
        #         self.knowledge.pop(ptr)
        #     else:
        #         ptr+=1

        "no need for cleanup checks if already poped befor queuing"

    def add_to_knowledge(self, sentence):
        if not (sentence.known_safes() or sentence.known_mines()):
            self.knowledge.append(sentence)
            return True
        
        self.mark_sentence(sentence)
        return False

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.mark_safe(cell)
        self.moves_made.add(cell)

        new_sen = Sentence(self.valid_neibers(cell), count)
        if not new_sen.cells: return 

        if self.add_to_knowledge(new_sen):
            return
        # else:
            # inference checking


        append_flag = True
        ini_ln = len(self.knowledge)
        ptr=0
        while ptr<ini_ln:
            sentence = self.knowledge[ptr]
            if len(new_sen.cells)>len(sentence.cells):
                ptr+=1 # not removing the current sendtence from knowledge
                if sentence.issubset(new_sen):
                    append_flag = False
                    inference = Sentence(new_sen - sentence, abs(new_sen.count - sentence.count))
                    self.add_to_knowledge(inference)

            else:# new_sen is smaller
                if new_sen.issubset(sentence):
                    inference = Sentence(sentence - new_sen, abs(new_sen.count - sentence.count))
                    self.knowledge.pop(ptr)
                    ini_ln-=1
                    self.add_to_knowledge(inference)
                else:
                    ptr+=1 # only in case not poped

        if append_flag: 
            self.knowledge.append(new_sen)

        print("knowledge size", len(self.knowledge))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for c in self.safes:
            if c not in self.moves_made:
                return c

    def random_cell(self):
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width - 1)
        return (i, j)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while 1:
            c = self.random_cell()
            if c in self.mines or c in self.moves_made: 
                continue

            # should i mark c as moves made
            return c


