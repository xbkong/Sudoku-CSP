import numpy as np
import random

easy = np.array([[0, 6, 1, 0, 0, 0, 0, 5, 2],
                 [8, 0, 0, 0, 0, 0, 0, 0, 1],
                 [7, 0, 0, 5, 0, 0, 4, 0, 0],
                 [9, 0, 3, 6, 0, 2, 0, 4, 7],
                 [0, 0, 6, 7, 0, 1, 5, 0, 0],
                 [5, 7, 0, 9, 0, 3, 2, 0, 6],
                 [0, 0, 4, 0, 0, 9, 0, 0, 5],
                 [1, 0, 0, 0, 0, 0, 0, 0, 8],
                 [6, 2, 0, 0, 0, 0, 9, 3, 0]])

medium = np.array([[5, 0, 0, 6, 1, 0, 0, 0, 0],
                   [0, 2, 0, 4, 5, 7, 8, 0, 0],
                   [1, 0, 0, 0, 0, 0, 5, 0, 3],
                   [0, 0, 0, 0, 2, 1, 0, 0, 0],
                   [4, 0, 0, 0, 0, 0, 0, 0, 6],
                   [0, 0, 0, 3, 6, 0, 0, 0, 0],
                   [9, 0, 3, 0, 0, 0, 0, 0, 2],
                   [0, 0, 6, 7, 3, 9, 0, 8, 0],
                   [0, 0, 0, 0, 8, 6, 0, 0, 5]])

hard = np.array([[0, 4, 0, 0, 2, 5, 9, 0, 0],
                 [0, 0, 0, 0, 3, 9, 0, 4, 0],
                 [0, 0, 0, 0, 0, 0, 0, 6, 1],
                 [0, 1, 7, 0, 0, 0, 0, 0, 0],
                 [6, 0, 0, 7, 5, 4, 0, 0, 9],
                 [0, 0, 0, 0, 0, 0, 7, 3, 0],
                 [4, 2, 0, 0, 0, 0, 0, 0, 0],
                 [0, 9, 0, 5, 4, 0, 0, 0, 0],
                 [0, 0, 8, 9, 6, 0, 0, 5, 0]])

evil = np.array([[0, 6, 0, 8, 2, 0, 0, 0, 0],
                 [0, 0, 2, 0, 0, 0, 8, 0, 1],
                 [0, 0, 0, 7, 0, 0, 0, 5, 0],
                 [4, 0, 0, 5, 0, 0, 0, 0, 6],
                 [0, 9, 0, 6, 0, 7, 0, 3, 0],
                 [2, 0, 0, 0, 0, 1, 0, 0, 7],
                 [0, 2, 0, 0, 0, 9, 0, 0, 0],
                 [8, 0, 4, 0, 0, 0, 7, 0, 0],
                 [0, 0, 0, 0, 4, 8, 0, 2, 0]])


# ---------------- Version 1 Backtracking only ----------------------------------
def find_unfilled(grid):
    res = np.where(grid == 0)
    if len(res[0]) == 0:
        return -1, -1
    idx = random.randint(0, len(res[0]) - 1)
    return res[0][idx], res[1][idx]


def get_unfilled(grid):
    res = np.where(grid == 0)
    res = zip(res[0], res[1])
    return res


def validate(grid, i, j, e):
    valid_row = not (e in grid[i])
    if valid_row:
        valid_col = not (e in grid[:, j])
        if valid_col:
            top_left_x = 3 * (i / 3)
            top_left_y = 3 * (j / 3)
            if e in grid[top_left_x:top_left_x+3, top_left_y:top_left_y+3]:
                return False
            return True
    return False

v1_counter = [0]

v1_unfilled = get_unfilled(easy)
random.shuffle(v1_unfilled)


def solver_v1(grid):
    if len(v1_unfilled) == 0:
        return True
    cell = v1_unfilled[-1]
    i = cell[0]
    j = cell[1]
    l = range(1, 10)
    random.shuffle(l)
    for e in l:
        if validate(grid, i, j, e):
            grid[i][j] = e
            v1_unfilled.pop()
            v1_counter[0] += 1
            if solver_v1(grid):
                return True
            grid[i][j] = 0
            v1_unfilled.append((i, j))

    return False

# --------------- End of Version 1 ----------------------------------------
# ---------------------- Version 2 ----------------------------------------


# Check for whether the value added is a critical (must have) value in the
# row, col or subgrid that the value belongs to
def neighbors_check(possible_values, value, row, col):
    # Check subgrid
    subgrid_x = row / 3
    subgrid_y = col / 3
    for i in range(3):
        for j in range(3):
            if subgrid_x * 3 + i == row and subgrid_y * 3 + j == col:
                continue
            neighbors = possible_values[subgrid_y * 3 + j + (subgrid_x * 3 + i) * 9]
            if len(neighbors) == 1 and value == neighbors[0]:
                return False
    # Check same row
    for i in range(9):
        if i == col:
            continue
        neighbors = possible_values[row * 9 + i]
        if len(neighbors) == 1 and value == neighbors[0]:
            return False
    # Check same col
    for i in range(9):
        if i == row:
            continue
        neighbors = possible_values[col + 9 * i]
        if len(neighbors) == 1 and value == neighbors[0]:
                return False

    return True


# Get a list of possible values for each cell
def get_possible_values(grid):
    possible_vals = []
    # initialize all remaining values to the full domain
    for i in range(81):
        possible_vals.append(range(1, 10))
    res = np.where(grid != 0)
    res = zip(res[0], res[1])
    for idx in res:
        if grid[idx[0]][idx[1]] != 0:
            value = grid[idx[0]][idx[1]]
            possible_vals = remove_values(idx[0], idx[1], value, possible_vals)

    return possible_vals


# Given that a certain cell contains a value, remove this value from
# the potential values for all cells in its row, column and the 3*3 grid it belongs to
def remove_values(row, col, value, possible_vals):
    possible_vals[col + row * 9] = [0]
    subgrid_x = row / 3
    subgrid_y = col / 3
    for i in range(3):
        for j in range(3):
            try:
                possible_vals[subgrid_y * 3 + j + (subgrid_x * 3 + i) * 9].remove(value)
            except ValueError:
                pass
    for i in range(9):
        try:
            possible_vals[row * 9 + i].remove(value)
        except ValueError:
            pass
    for i in range(9):
        try:
            possible_vals[col + 9 * i].remove(value)
        except ValueError:
            pass

    return possible_vals


def solver_v2(grid):
    i, j = find_unfilled(grid)

    # No empty cells means success
    if i == -1 and j == -1:
        return True

    possible_vals = get_possible_values(grid)

    # Only use values within the possible values list
    values = possible_vals[j + i * 9]
    random.shuffle(values)
    for value in values:
        if neighbors_check(possible_vals, value, i, j):
            grid[i][j] = value
            v1_counter[0] += 1
            if solver_v2(grid):
                return True
            grid[i][j] = 0
    return False

# --------------- End of Version 2 ----------------------------------------
# ---------------------- Version 3 ----------------------------------------


# Tabulate number of constraining values for each potential
def tabulate_constraining_count(values, possible_vals, row, col):
    res = []

    for value in values:
        count = 0
        subgrid_x, subgrid_y = row / 3, col / 3

        for i in range(3):
            for j in range(3):
                if [subgrid_x * 3 + i, subgrid_y * 3 + j] == [row, col]:
                    continue
                if value in possible_vals[subgrid_y * 3 + j + (subgrid_x * 3 + i) * 9]:
                    count += 1

        count += sum(1 for i in range(9) if i != col and value in possible_vals[row * 9 + i])
        count += sum(1 for i in range(9) if i != row and value in possible_vals[col + 9 * i])

        res.append(count)

    return res


def count_constraints(cell, grid):
    count = 0
    row, col = cell[0], cell[1]
    subgrid_x, subgrid_y = row / 3, col / 3
    for i in range(3):
        for j in range(3):
            if subgrid_x * 3 + i == row and subgrid_y * 3 + j == col:
                continue
            if grid[subgrid_x * 3 + i][subgrid_y * 3 + j] == 0:
                count += 1

    count += sum(1 for i in range(9) if i != col and grid[row][i] == 0)
    count += sum(1 for i in range(9) if i != row and grid[i][col] == 0)

    return count


# Count remaining values for each cell and get a list of mcvs
def get_mcv_cells(unfilled_cells, possible_values):
    remaining_val_count = []
    for cell in unfilled_cells:
        remaining_val_count.append(len(possible_values[cell[0] * 9 + cell[1]]))
    mcv_cells = []
    minimum = min(remaining_val_count)
    for i in range(len(remaining_val_count)):
        value = remaining_val_count[i]
        if value == minimum:
            mcv_cells.append(unfilled_cells[i])
    return mcv_cells


def get_target_cell(mcv_cells, grid):
    cell = mcv_cells[0]
    if len(mcv_cells) != 1:
        # Choose variable with most constraints on others (most constraining)
        constraints_count = []
        for cell in mcv_cells:
            count = count_constraints(cell, grid)
            constraints_count.append(count)
            max_count = max(constraints_count)
            for i in range(len(constraints_count)):
                value = constraints_count[i]
                if value == max_count:
                    cell = mcv_cells[i]
                    break
    return cell


# V3, backtracking with forward checking and 3 heuristics
# Most constrained variable, Most constraining variable, and least constraining value heuristics
def solver_v3(grid):
    unfilled_cells = get_unfilled(grid)
    if len(unfilled_cells) == 0:
        return True

    possible_values = get_possible_values(grid)
    mcv_cells = get_mcv_cells(unfilled_cells, possible_values)
    # Get the first most constraining cell from most constrained cells
    cell = get_target_cell(mcv_cells, grid)
    row, col = cell[0], cell[1]

    values = list(possible_values[col + row * 9])

    while len(values) != 0:
        # Count number of constraining vals for each and take the minimum
        cv_list = tabulate_constraining_count(values, possible_values, row, col)
        idx = cv_list.index(min(cv_list))
        value = values[idx]
        values.remove(value)
        if neighbors_check(possible_values, value, row, col):
            grid[row][col] = value
            v1_counter[0] += 1
            if solver_v3(grid):
                return True
            # Backtrack
            grid[row][col] = 0

    return False


def solve_and_print(solver):
    solver(easy)
    solver(medium)
    solver(hard)
    solver(evil)
    print "EASY:"
    print easy
    print "MEDIUM:"
    print medium
    print "HARD:"
    print hard
    print "EVIL:"
    print evil
