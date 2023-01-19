# Lucas Wenger
# 6/3/2021
# Sudoku Solver
# v2 Takes the approach of eliminating candidates rather than filling in single blanks. This takes more time but can solve
# significantly more complicated puzzles.

# SAMPLE PUZZLE WITH UNIQUE SOLUTION TO COPY FOR TEST:
# "xxxxxxxxx87x3xxxxxxxxx42x95xxx29x1xxx2xxxx57xxxx1x486xxx9xxxxx876xx18xxxxxxxxxx3x"

# Sudoku class
class Sudoku:
    """Class made to aid in solving sudoku puzzles"""
    
    def __init__(self, nums):
        """Note: nums should be a string of 81 characters with lower case x's in place of blanks"""
        if len(nums) != 81:
            print("ERROR: puzzle must be 81 characters")
            exit()
        for num in nums:
            if num not in ['x','1','2','3','4','5','6','7','8','9']:
                print("ERROR: puzzle must consist only of digits 1-9 and lower case x's")
                exit()
        nums = self._splitlist(list(nums), 9)
        for rowindex, row in enumerate(nums):
            for valueindex, value in enumerate(row):
                if value == 'x':
                    nums[rowindex][valueindex] = ['1','2','3','4','5','6','7','8','9']
        self.puzzle = nums
        # Note: Now, self.puzzle[1][2] corresponds to the list of candidates for row index 1, column index 2

    @staticmethod
    def _splitlist(lyst, splitlength):
        """Takes a list as an argument and returns the same list, split into sublists of length splitlength"""
        splitlength = int(splitlength)
        if type(lyst) != list:
            print("ERROR: arg type must be list")
            exit()
        if len(lyst) % splitlength != 0:
            print("ERROR: length of list must be divisible by splitlength")
            exit()
        numlists = int(len(lyst)/splitlength)
        newlyst = [[] for i in range(numlists)]
        counter = 0
        for l in range(numlists):
            newlyst[l] = lyst[counter:splitlength+counter]
            counter += splitlength
        return newlyst

    # Collection of functions for easy viewing of rows, cols, and blocks -- ex: self._row(0)
    # refers to the first row of the physical puzzle

    def _row(self, a):
        """Returns list that represents row a"""
        if a not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid row number -- index must be between 0 and 8, inclusive")
            return
        else:
            templist = []
            for num in self.puzzle[a]:
                templist.append(num)
            return templist
    
    def _col(self, a):
        """Returns list that represents col a"""
        if a not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid row number -- index must be between 0 and 8, inclusive")
            return
        else:
            templist = []
            for num in range(0,9):
                templist.append(self.puzzle[num][a])
            return templist

    def _block(self, a):
        """Returns list that represents block a where blocks are ordered:
            [0][1][2]
            [3][4][5]
            [6][7][8]
            NOTE: Blocks of a puzzle and values within a block both follow the above indexing scheme"""
        if a not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid row number -- index must be between 0 and 8, inclusive")
            return
        else:
            templist = []
            for row in range(3*(a//3), (3*(a//3))+3):
                for col in range(3*(a%3),(3*(a%3))+3):
                    templist.append(self.puzzle[row][col])
            return templist
    # Note: Returns a duplicate list of row, col, or block values

    # UNUSED in this version
    def _blocktorc(self, block, index):
        """Takes a block number and an index and finds the (row, col) notation for that index"""
        if block not in [0,1,2,3,4,5,6,7,8] or index not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid block or index number -- block and index must be between 0 and 8, inclusive")
            return
        else:
            # Conjecture: In an nxn square notated like our square here, index i can be found at row i//n and col i%n.
            # It at least works here! 
            row = index // 3
            col = index % 3
            # Now row/col is accurate for block 0
            row += (block//3)*3
            col += (block%3)*3
            # Now row/col is accurate for the correct block
            return (row, col)

    def _rctoblock(self, row, col):
        """Takes a (row, col) notation and returns the block number that contains that value"""
        if row not in [0,1,2,3,4,5,6,7,8] or col not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid row or col number -- row and col must be between 0 and 8, inclusive")
            return
        else:
            block = ((row//3)*3) + (col//3)
            return block

    # UNUSED in this version
    @staticmethod
    def _missingnos(templist):
        """Takes a list as an argument and outputs a list of any missing numbers 1-9"""
        iterlist = ['1','2','3','4','5','6','7','8','9']
        missingvals = list(iterlist)
        for num in iterlist:
            if num in templist:
                missingvals.remove(num)
        return missingvals
        
    
    # Now we get to real sudoku strategies
    def _same_rcb(self):
        """Eliminates values in same row, col, or block from candidate lists"""
        for rowindex, row in enumerate(self.puzzle):
            for valueindex, value in enumerate(row):
                if type(value) == list:
                    # Eliminate vals in same row
                    for candidate in self._row(rowindex):
                        if candidate in value:
                            value.remove(candidate)
                    # Eliminate vals in same col
                    for candidate in self._col(valueindex):
                        if candidate in value:
                            value.remove(candidate)
                    # Eliminate vals in same block
                    for candidate in self._block(self._rctoblock(rowindex, valueindex)):
                        if candidate in value:
                            value.remove(candidate)
        return
        
    def _lone_candidate(self):
        """If an unknown value contains the only instance of a candidate in a row/col/block, eliminates all other candidates in the list"""
        for rowindex, row in enumerate(self.puzzle):
            for valueindex, value in enumerate(row):
                if type(self.puzzle[rowindex][valueindex]) == list:
                    # Check row
                    if len(self.puzzle[rowindex][valueindex]) > 1:
                        numcandidates = {str(num):0 for num in range(1,10)}
                        for unknowns in self._row(rowindex):
                            if type(unknowns) == list:
                                for can in unknowns:
                                    numcandidates[can] += 1
                        for can in numcandidates:
                            if numcandidates[can] == 1 and can in self.puzzle[rowindex][valueindex]:
                                self.puzzle[rowindex][valueindex] = [can]
                                # Note: Could use can instead of [can] for some added efficiency, but then there would be vals updating
                                # outside of _update_vals -- it's a choice of speed vs. organization
                    # Check col
                    if len(self.puzzle[rowindex][valueindex]) > 1:
                        numcandidates = {str(num):0 for num in range(1,10)}
                        for unknowns in self._col(valueindex):
                            if type(unknowns) == list:
                                for can in unknowns:
                                    numcandidates[can] += 1
                        for can in numcandidates:
                            if numcandidates[can] == 1 and can in self.puzzle[rowindex][valueindex]:
                                self.puzzle[rowindex][valueindex] = [can]
                    #Check block
                    if len(self.puzzle[rowindex][valueindex]) > 1:
                        numcandidates = {str(num):0 for num in range(1,10)}
                        for unknowns in self._block(self._rctoblock(rowindex, valueindex)):
                            if type(unknowns) == list:
                                for can in unknowns:
                                    numcandidates[can] += 1
                        for can in numcandidates:
                            if numcandidates[can] == 1 and can in self.puzzle[rowindex][valueindex]:
                                self.puzzle[rowindex][valueindex] = [can]
        return

    # Now we update the lists with single values to be single-character strings
    def _update_vals(self):
        """Replaces single-candidate lists with single-value strings and returns True/False depending whether any values have changed"""
        anychanges = False
        for rowindex, row in enumerate(self.puzzle):
            for valueindex, value in enumerate(row):
                if type(value) == list:
                    if len(value) == 1:
                        self.puzzle[rowindex][valueindex] = value[0]
                        anychanges = True
        return anychanges

        
    #TODO: Add other techniques



    @classmethod
    def solve(cls, nums):
        """Put it all together and solve the puzzle (if possible)!"""
        puzz = cls(nums)
        processing = True
        while processing:
            puzz._same_rcb()
            puzz._lone_candidate()
            processing = puzz._update_vals()
        try:
            for i in range(17):
                if i%2 == 0:
                    print(" | ".join(puzz.puzzle[int(i/2)]))
                elif i%2 == 1:
                    print("---------------------------------")
        except TypeError:
            print("Sudoku puzzle not completely solved! Aborting program.")
        return

        

                    
                
                    
            
    
        
