assignments = []

def get_units(box):
    return [u for u in units if box in u]

def get_peers(box):
    return set([b for u in get_units(box) for b in u if b != box])

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in units:
        # Get all two-element boxes
        all_twins = [values[box] for box in unit if len(values[box]) == 2]

        twins = []
        naked_twins = []
        # Get all values that repeat
        for val in all_twins:
            if val in twins:
                naked_twins.append(val)
            else:
                twins.append(val)       

        naked_twins = ''.join(set(naked_twins))

        # Remove naked twins
        for val in naked_twins:
            for box in [k for k in unit if values[k] not in naked_twins]:
                values = assign_value(values, box, values[box].replace(val, ""))

    return values



def cross(A, B):
    "Cross product of elements in A and elements in B."
    vals = []
    for a in A:
        for b in B:
            vals.append(a+b)
    return vals

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    boxes = cross(row_names, col_names)
    grid = [col_names if val == '.' else val for val in grid]
    return dict(zip(boxes, grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    if values == False:
        return False

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in row_names:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in col_names))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in get_peers(box):
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in units:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        #print("\n\n-----------\n\n")
        #display(values)
        values = eliminate(values)
        #print("Eliminate")
        #display(values)
        values = only_choice(values)
        #print("OC")
        #display(values)
        values = naked_twins(values)
        #print("NT")
        #display(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        # If no possible values left for any box, not right soln
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Turn into dictionary representation
    assert len(grid) == 81
   
    return search(grid_values(grid)) 

'''
Define some constants.
'''
row_names = 'ABCDEFGHI'
col_names = '123456789'

# Get all units
rows = [cross(r, col_names) for r in row_names]
cols = [cross(row_names, c) for c in col_names]
squares = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diags = [[a+b for a,b in zip(row_names, col_names)], 
[a+b for a,b in zip(row_names[::-1], col_names)]] 
units = rows + cols + squares + diags

boxes = cross(row_names, col_names)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
