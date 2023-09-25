import numpy as np
import random

class Sudoku:

    sudoku_log = {}
    move_log = {}
    coordinates_log = {}
    move_number = 0

    def possible(i, j, n, grid):
        Sudoku.coordinates_log[1] = []
        for x in range(9):
            if grid[i][x] == n:
                Sudoku.move_log[Sudoku.move_number].append("Odigravanje broja " + str(n) + " na poziciji " + str(i+1) + ", " + str(j+1) + " je nemoguće jer se broj " + str(n) + " već nalazi u redu " + str(i+1)  + ".")
                return False
        for x in range(9):
            if grid[x][j] == n:
                Sudoku.move_log[Sudoku.move_number].append("Odigravanje broja " + str(n) + " na poziciji " + str(i+1) + ", " + str(j+1) + " je nemoguće jer se broj " + str(n) + " već nalazi u koloni " + str(j+1) + ".")
                return False
        x0 = (i//3)*3
        y0 = (j//3)*3
        for x in range(3):
            for y in range(3):
                if grid[x0+x][y0+y] == n:
                    Sudoku.move_log[Sudoku.move_number].append("Odigravanje broja " + str(n) + " na poziciji " + str(i+1) + ", " + str(j+1) + " je nemoguće jer se broj " + str(n) + " već nalazi u kvadratu " + str(x0+1) + ", " + str(y0+1) + "." )
                    return False
        Sudoku.move_log[Sudoku.move_number].append("Odigravanje broja " + str(n) + " na poziciji " + str(i+1) + ", " + str(j+1) + " je moguće jer se broj " + str(n) + " ne nalazi u redu " + str(i+1) + ", koloni " + str(j+1) + " ili kvadratu " + str(x0+1) + ", " + str(y0+1) + "." )
        return True
        
    def solve(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    Sudoku.move_number += 1
                    Sudoku.sudoku_log[Sudoku.move_number] = np.copy(grid)
                    Sudoku.move_log[Sudoku.move_number] = []
                    Sudoku.coordinates_log[Sudoku.move_number+1] = []
                    Sudoku.coordinates_log[Sudoku.move_number+1].append([i, j])
                    for n in range(1, 10):
                        if Sudoku.possible(i, j, n, grid):
                            grid[i][j] = n
                            if Sudoku.solve(grid):
                                return True
                            grid[i][j] = 0
                            Sudoku.move_log[Sudoku.move_number].append("Backtrack na poziciji " + str(i+1) + ", " + str(j+1) + " jer broj " + str(n) + " ipak nije moguć na toj poziciji." )
                            Sudoku.coordinates_log[Sudoku.move_number+1].append([i, j])
                    return False
        return True 
    
    def shuffle_sudoku_numbers():
        return random.sample(range(1, 10), 9)

    def sudoku_generator(difficulty_level):
        grid = np.zeros((9, 9), dtype=int)

        grid[0] = Sudoku.shuffle_sudoku_numbers()
        Sudoku.coordinates_log[1] = []
        Sudoku.solve(grid)

        puzzle = np.copy(grid)
        num_cells_to_remove = int(81 * (1 - difficulty_level))

        cells_to_remove = random.sample(range(81), num_cells_to_remove)
        for cell in cells_to_remove:
            i, j = divmod(cell, 9)
            backup = puzzle[i][j]
            puzzle[i][j] = 0
            temp_grid = np.copy(puzzle)

            if not Sudoku.solve(temp_grid):
                puzzle[i][j] = backup

        Sudoku.move_log = {}
        Sudoku.sudoku_log = {}
        Sudoku.coordinates_log = {}
        Sudoku.move_number = 0 
        return puzzle
    