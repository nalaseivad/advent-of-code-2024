import sys


def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end = '')
        print()


def count_x_mas_in_grid(grid, grid2):
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    def update_grid2(r, c):
        grid2[r][c] = grid[r][c]
        grid2[r - 1][c - 1] = grid[r - 1][c - 1]
        grid2[r + 1][c + 1] = grid[r + 1][c + 1]
        grid2[r - 1][c + 1] = grid[r - 1][c + 1]
        grid2[r + 1][c - 1] = grid[r + 1][c - 1]

    def cell_in_bounds(r, c):
        return 0 <= r < num_rows and 0 <= c < num_cols

    # Check that the X, centered at (r, c), is all in bounds
    def x_in_bounds(r, c):
        if not cell_in_bounds(r, c): return 0
        if not cell_in_bounds(r - 1, c - 1): return 0
        if not cell_in_bounds(r + 1, c + 1): return 0
        if not cell_in_bounds(r - 1, c + 1): return 0
        if not cell_in_bounds(r + 1, c - 1): return 0
        return 1

    # A
    #  B
    #   C
    def check_leading_diagonal(r, c, word):
        if grid[r - 1][c - 1] == word[0] and grid[r][c] == word[1] and grid[r + 1][c + 1] == word[2]:
            return 1
        return 0

    #   C
    #  B
    # A
    def check_trailing_diagonal(r, c, word):
        if grid[r + 1][c - 1] == word[0] and grid[r][c] == word[1] and grid[r - 1][c + 1] == word[2]:
            return 1
        return 0

    # A C    A A    C C    C A
    #  B  or  B  or  B  or  B
    # A C    C A    A A    C A
    def check_x(r, c, word):
        rev_word = word[::-1]
        result = check_leading_diagonal(r, c, word) or check_leading_diagonal(r, c, rev_word)
        result = result and (check_trailing_diagonal(r, c, word) or check_trailing_diagonal(r, c, rev_word))
        return result

    def is_x_mas(r, c):
        if grid[r][c] != 'A': return 0
        if not x_in_bounds(r, c): return 0
        if check_x(r, c, "MAS"):
            update_grid2(r, c)
            return 1
        return 0

    count = 0
    for r in range(num_rows):
        for c in range(num_cols):
            count += is_x_mas(r, c)
    return count


def count_xmas_in_grid(grid, grid2):
    word = "XMAS"
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    word_len = len(word)

    directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

    def cell_in_bounds(r, c):
        return 0 <= r < num_rows and 0 <= c < num_cols

    def search(r, c, index, dr, dc):
        if index == word_len:
            return 1
        if (not cell_in_bounds(r, c)) or (grid[r][c] != word[index]):
            return 0
        found = search(r + dr, c + dc, index + 1, dr, dc)
        if(found):
            grid2[r][c] = grid[r][c]
        return found

    count = 0
    for r in range(num_rows):
        for c in range(num_cols):
            for dr, dc in directions:
                count += search(r, c, 0, dr, dc)
    return count


def part_1(grid):
    grid2 = [["." for _ in range(len(grid))] for _ in range(len(grid[0]))]
    count = count_xmas_in_grid(grid, grid2)
    print_grid(grid2)
    print()
    return count


def part_2(grid):
    grid2 = [["." for _ in range(len(grid))] for _ in range(len(grid[0]))]
    count = count_x_mas_in_grid(grid, grid2)
    print_grid(grid2)
    print()
    return count


def part_n(file_path, fn):
    grid = []
    with open(file_path, "r") as lines:
        for row in (line.rstrip("\n") for line in lines):
            grid.append(list(row))
    print(fn(grid))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
