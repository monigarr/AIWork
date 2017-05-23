assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
#square = 1 digit
#unit = 9 squares
#grid = 81 squares
#peers = ea square next to, above, below and diagnal to current square

#########################################
#   assign_value
#
#   Use this function to update values dictionary.
#   Assigns a value to a given square. 
#       If value updates the board records it.
#
#########################################
def assign_value(values, square, value):
    # If values don't change - don't append actions.
    if values[square] == value:
        return values

    values[square] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


#########################################
#   naked_twins
#
#   Eliminate values using naked twins strategy.
#       Args:
#           values(dict): a dictionary of the form {'box_name': '123456789', ...}
#   
#       Returns:
#           the values dictionary with the naked twins eliminated from peers.
# 
#   When 2 or more possible solutions available:
#   same digit might work in 2 or more squares
#       Branch out & consider all solutions
#       One answer might provide 3 more answers
#       Branch out for each of those answers
#       Create Tree of possible answers
#       Traverse tree until we find ONE solution
#
#########################################
def naked_twins(values):
    # Find all naked twins / length of values is 2
    nakedtwin = [square for square in values.keys() if len(values[square]) == 2]   
    
    #for each square with nakedtwin
    for square in nakedtwin:
        # get value of square digit
        digit = values[square]
        # compare all other squares within unit for matching digit
        for unit in units[square]:
            for x in unit:
                # if digit and twin match and not on same unit
                if (digit == values[x] and square != x):
                    # set twin digit to twindigit
                    twindigit = values[x]
                    
                    # for each unit with twin, update values
                    for y in unit:
                        if(y != square and y != x):
                            values[y] = values[y].replace(twindigit[0],'')
                            if(len(twindigit) > 1):
                                values[y] = values[y].replace(twindigit[1],'')
    
    # Eliminate twins as options for peers
    return values


#########################################
#   cross
#
#   Create Squares, Units and Peers
#   cross product of elements 
#       in A and elements in B
#
#########################################
def cross(A, B):
    return [a + b for a in A for b in B]


#########################################
#   Game Board Definitions
#########################################
squares         = cross(rows, cols)

#prep for cleaner unitlist definition
row_units       = [cross(r, cols)   for r in rows]
column_units    = [cross(rows, c)   for c in cols]
square_units    = [cross(rs, cs)    for rs in ('ABC','DEF','GHI')   for cs in ('123','456','789')]
#A1, B2, C3, D4...I9
diag1           = [[a[0]+a[1]       for a in zip(rows,cols)]]
#A9, B8, C7, D6...I1
diag2           = [[a[0]+a[1]       for a in zip(rows,cols[::-1])]]

#top row A1 ... A9 bottom row I1 to I9
unitlist        = row_units + column_units + square_units + diag1 + diag2

# dictionary. ea square maps to list of units that have the square
units           = dict((s, [u for u in unitlist if s in u]) for s in squares)
# dictionary. ea square maps to set of squares formed by union of squares in units of s, but NOT s itself
peers           = dict((s, set(sum(units[s],[]))-set([s])) for s in squares)


#########################################
#   grid_values
#
#   Convert grid string into dictionary 
#       {square: char} with '123456789' for empties.
#   Input:  grid string
#   Output: grid dictionary
#       Keys:   squares, e.g., 'A1' or 'A2'
#       Values: value in each square e.g., '8' or '1'. 
#       If square has no value, then value will be '123456789'.
#
#########################################
def grid_values(grid):
    chars   = []
    digits  = cols

    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(squares, chars))
    

#########################################
#   display
#
#   Display values as 2-D grid.
#   Input:  sudoku dictionary
#   Output: None
#
#########################################
def display(values):
    width   = 1 + max(len(values[s]) for s in squares)
    line    = '+'.join(['-' * (width * 3)] *3)

    for r in rows:
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


#########################################
#   eliminate
#
#   Constraint Propogation
#   Go through all squares, 
#       find constraints for each square (possible answers)
#   Iteratively repeat to narrow possible answers.
#   if square has a digit, 
#       remove digit from all peers.
#   if square has only one possible digit solution
#       put digit in that square.
#
#   Input:  sudoku dictionary
#   Output: sudoku dictionary
#
#########################################
def eliminate(values):
    solved_values   = [square for square in values.keys() if len(values[square]) == 1]
    
    for square in solved_values:
        digit = values[square]
        
        for peer in peers[square]:
            values[peer] = values[peer].replace(digit,'')
    return values


#########################################
#   only_choice
#
#   Go through all units, if unit has digit that 
#   is only answer for only one square,
#       assign the digit to that square
#   unitlist considers all peers of current square:
#       next to, above, below and diagnal
#   Input:  sudoku dictionary
#   Output: sudoku dictionary 
#
#########################################
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [square for square in unit if digit in values[square]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


#########################################
#   reduce_puzzle
#   
#   Iteratively run eliminate() and only_choice(). 
#   If a square has no available values, return False.
#   If sudoku is solved, return sudoku.
#   If after an iteration of both functions and sudoku remains the same, return sudoku.
#   Input:     sudoku dictionary
#   Output:    sudoku dictionary
#
#########################################
def reduce_puzzle(values):
    solved_values   = [square for square in values.keys() if len(values[square]) == 1]

    stalled         = False

    while not stalled:
        solved_values_before = len([square for square in values.keys() if len(values[square]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        # values = naked_twins(values)
        solved_values_after = len([square for square in values.keys() if len(values[square]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([square for square in values.keys() if len(values[square]) == 0]):
            #print('Failed in reduce_puzzle')
            return False
    return values


#########################################
#   search
#
#   Try all possible solutions until we 
#   hit solution that works
#   If 2 or more possible solutions:
#       Branch out & consider all solutions
#       Create Tree of possible solutions
#       Traverse Tree until we find the solution
#
#########################################
def search(values):
    "Using depth-first search and propagation, try all possible values."
    
    # Reduce puzzle
    values = reduce_puzzle(values)   

    if values is not False:
        display(values)
        naked_twins(values)
    if values is False:
        #print('Failed')
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares): 
        return values ## Solved!
    
    # Choose one unfilled square with fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    # Use recurrence to solve each resulting sudoku 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    

#########################################
#   solve
#
#   Find Sudoku grid solution (string)
#   Args:
#       Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
#   Returns:
#       dictionary of final sudoku grid. 
#       False if no solution exists.
#
#########################################
def solve(grid):
    #convert grid into dictionary
    values = grid_values(grid)
    #pass converted grid into search()
    values = search(values)
    
    return values    

if __name__ == '__main__':
    #diag_sudoku_grid = '........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2.'
    #diag_sudoku_grid = '...7.9....85...31.2......7...........1..7.6......8...7.7.........3......85.......'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))
    
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
