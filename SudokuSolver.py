# Lucas Wenger
# 6/3/2021
# Sudoku Solver

# SAMPLE PUZZLE WITH UNIQUE SOLUTION TO COPY FOR TEST:
# "1x6xxxx5xx7xx3xxx4x9xxx52xxxx2x6xxx7xxx1x8xxxx47x2xxxxxxxxxx8x3xx32xxxx6xxxxxxxx2"
# SAMPLE PUZZLE THAT CAN BE SOLVED WITH JUST OPEN SINGLES: 
# "xxxxx138x87x3694x131x842x9565829x1x3x2468357x9371x4862249x3561876x918x545814xx93x"

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
                if num in ['1','2','3','4','5','6','7','8','9']:
                    templist.append(num)
                else:
                    templist.append('0')
            return templist

    def _col(self, a):
        """Returns list that represents col a"""
        if a not in [0,1,2,3,4,5,6,7,8]:
            print("ERROR: invalid row number -- index must be between 0 and 8, inclusive")
            return
        else:
            templist = []
            for num in range(0,9):
                if self.puzzle[num][a] in ['1','2','3','4','5','6','7','8','9']:
                    templist.append(self.puzzle[num][a])
                else:
                    templist.append('0')
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
                    if self.puzzle[row][col] in ['1','2','3','4','5','6','7','8','9']:
                        templist.append(self.puzzle[row][col])
                    else:
                        templist.append('0')
            return templist
    # Note: Returns a list of row, col, or block with known values filled in and unknown values replaced with "0"

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
            return (row, col)
    
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
    def _open_singles(self):
        """For single empty space in row, col, or block"""
        opensingles = True
        while opensingles:
            opensingles = False
            for num in range(0,9):
                # Rows
                if len(self._missingnos(self._row(num))) == 1:
                    opensingles = True
                    # set open single to the one missing value from that row
                    self.puzzle[num][self._row(num).index("0")] = self._missingnos(self._row(num))[0]
                # Cols
                if len(self._missingnos(self._col(num))) == 1:
                    opensingles = True
                    # set open single to the one missing value from that col
                    self.puzzle[self._col(num).index("0")][num] = self._missingnos(self._col(num))[0]
                #Blocks
                if len(self._missingnos(self._block(num))) == 1:
                    opensingles = True
                    # set open single to the one missing value from that block
                    self.puzzle[self._blocktorc(num,self._block(num).index("0"))[0]][self._blocktorc(num,self._block(num).index("0"))[1]] = self._missingnos(self._block(num))[0]
        return

    #TODO: Add visual_elimination and other techniques



    @classmethod
    def solve(cls, nums):
        puzz = Sudoku(nums)
        puzz._open_singles()
        try:
            for i in range(17):
                if i%2 == 0:
                    print(" | ".join(puzz.puzzle[int(i/2)]))
                elif i%2 == 1:
                    print("---------------------------------")
        except TypeError:
            print("Sudoku puzzle not completely solved! Aborting program.")
        return
