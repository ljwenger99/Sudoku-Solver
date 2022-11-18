# Lucas Wenger
# 6/3/2021
# Sudoku Solver

# SAMPLE PUZZLE WITH UNIQUE SOLUTION TO COPY FOR TEST:
# "1x6xxxx5xx7xx3xxx4x9xxx52xxxx2x6xxx7xxx1x8xxxx47x2xxxxxxxxxx8x3xx32xxxx6xxxxxxxx2"


# Helper function
def splitlist(lyst, splitlength):
    # Takes a list as an argument and returns the same list, split into sublists of length splitlength
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

class Sudoku:
    '''Class made to aid in solving sudoku puzzles'''
    def __init__(self, nums):
        '''Note: nums should be a string of 81 characters with lower case x's in place of blanks'''
        if len(nums) != 81:
            print("ERROR: puzzle must be 81 characters")
            exit()
        for num in nums:
            if num not in [x,1,2,3,4,5,6,7,8,9]:
                print("ERROR: puzzle must consist only of digits 1-9 and lower case x's")
                exit()
        nums = splitlist(list(nums), 9)
        for row in nums:
            for col in nums:
                if nums[row][col] == 'x':
                    nums[row][col] = [1,2,3,4,5,6,7,8,9]
        self.puzzle = nums
        # Note: Now, self.puzzle[1][2] corresponds to the list of candidates for row 2, column 3

        # Collection of functions for easy reference to rows, cols, and blocks -- ex: row(1) refers to the first row of the physical puzzle
        def _row(a):
            if a not in [1,2,3,4,5,6,7,8,9]:
                print("ERROR: invalid row number -- must be between 1 and 9")
                return
            else:
                for num in self.puzzle[a-1]:
                    if num in ['1','2','3','4','5','6','7','8','9']:
                        templist.append(num)
                    else:
                        templist.append('0')
                return templist

        def _col(a):
            if a not in [1,2,3,4,5,6,7,8,9]:
                print("ERROR: invalid row number -- must be between 1 and 9")
                return
            else:
                templist = []
                for num in range(1,10):
                    if self.puzzle[num][a] in ['1','2','3','4','5','6','7','8','9']:
                        templist.append(self.puzzle[num][a])
                    else:
                        templist.append('0')
                return templist

        def _block(a):
            if a not in [1,2,3,4,5,6,7,8,9]:
                print("ERROR: invalid row number -- must be between 1 and 9")
                return
            else:
                templist = []
                if a % 3 == 0:
                    for row in range(a-3, a):
                        for col in range(6,9):
                            if self.puzzle[row][col] in ['1','2','3','4','5','6','7','8','9']:
                                templist.append(self.puzzle[row][col])
                            else:
                                templist.append('0')
                elif a % 3 == 1:
                    for row in range(a-1, a+2):
                        for col in range(0,3):
                            if self.puzzle[row][col] in ['1','2','3','4','5','6','7','8','9']:
                                templist.append(self.puzzle[row][col])
                            else:
                                templist.append('0')
                elif a % 3 == 2:
                    for row in range(a-2, a+1):
                        for col in range(3,6):
                            if self.puzzle[row][col] in ['1','2','3','4','5','6','7','8','9']:
                                templist.append(self.puzzle[row][col])
                            else:
                                templist.append('0')
                else:
                    print("ERROR: something went wrong in block function")
                    return
                return templist

            # Now we get to real sudoku strategies
            def open_singles(self):
                '''For single empty space in row, col, or block'''
                opensingles = True
                while opensingles:
                    anysingles = False
                    # rows
                    for num in range(1,10):
                        numzeros = 0
                        for val in _row(num):
                            if val == '0':
                                numzeros += 1
                        if numzeros == 1:
                            anysingles = True
                            # NOTE FOR NEXT TIME: now we fix the open single and do the same for cols and blocks
                    
                
                    
            
    
        
