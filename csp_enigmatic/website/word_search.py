import random
from typing import List
import string

class WordSearch:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = []
        self.added_words = []

    def add_word(self, word: str):
        if len(self.words) == 10:
            raise ValueError("Word search can only contain 10 words.")
        else:
            if len(word) > self.size:
                raise ValueError("Word length exceeds grid size.")
            self.words.append(word)

    def generate(self) -> List[List[str]]:
        if not self.words:
            self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
            return self.grid
        for word in self.words:
            self._place_word(word)
        self._fill_empty_cells()
        return self.grid

    def _place_word(self, word: str):
        for _ in range(100):
            i, j, direction = self._random_position_direction(word)
            if self._can_place_word(word, i, j, direction):
                self._place_word_in_grid(word, i, j, direction)
                break

    def _random_position_direction(self, word: str):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        valid_directions = [
            'horizontal', 'vertical', 'diagonal',
            'horizontal_reverse', 'vertical_reverse',
            'diagonal_reverse_top_left', 'diagonal_reverse_top_right',
            'diagonal_reverse_bottom_left', 'diagonal_reverse_bottom_right'
        ]
        direction = random.choice(valid_directions)
        return i, j, direction

    def _can_place_word(self, word: str, i: int, j: int, direction: str) -> bool:
        di, dj = self._get_direction_change(direction)
        word_len = len(word)

        if (
            i + di * (word_len - 1) < 0 or
            i + di * (word_len - 1) >= self.size or
            j + dj * (word_len - 1) < 0 or
            j + dj * (word_len - 1) >= self.size
        ):
            return False

        for k in range(word_len):
            cell_value = self.grid[i + k * di][j + k * dj]
            if cell_value != ' ' and cell_value != word[k]:
                return False

        return True

    def _place_word_in_grid(self, word: str, i: int, j: int, direction: str):
        di, dj = self._get_direction_change(direction)
        for k in range(len(word)):
            self.grid[i + k * di][j + k * dj] = word[k]
        self.added_words.append(word)

    def _get_direction_change(self, direction: str):
        if direction == 'horizontal':
            return 0, 1
        elif direction == 'vertical':
            return 1, 0
        elif direction == 'diagonal':
            return 1, 1
        elif direction == 'horizontal_reverse':
            return 0, -1
        elif direction == 'vertical_reverse':
            return -1, 0
        elif direction == 'diagonal_reverse_top_left':
            return -1, -1
        elif direction == 'diagonal_reverse_top_right':
            return -1, 1
        elif direction == 'diagonal_reverse_bottom_left':
            return 1, -1
        elif direction == 'diagonal_reverse_bottom_right':
            return 1, 1
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def _fill_empty_cells(self):
        alphabet = string.ascii_uppercase
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = random.choice(alphabet)
    
    def solve(self):
        solved_grid = [[{'letter': self.grid[i][j], 'found': False} for j in range(self.size)] for i in range(self.size)]

        for word in self.words:
            found = False

            for i in range(self.size):
                for j in range(self.size):
                    for direction in [
                                        'horizontal', 'vertical', 'diagonal',
                                        'horizontal_reverse', 'vertical_reverse',
                                        'diagonal_reverse_top_left', 'diagonal_reverse_top_right',
                                        'diagonal_reverse_bottom_left', 'diagonal_reverse_bottom_right'
                                    ]:
                        if self._check_word_in_direction(word, i, j, direction):
                            self._mark_word_in_direction(solved_grid, word, i, j, direction)
                            found = True
                            break

                    if found:
                        break

                if found:
                    break

        return solved_grid

    def _check_word_in_direction(self, word, i, j, direction):
        di, dj = self._get_direction_change(direction)
        word_len = len(word)

        if (
            i + di * (word_len - 1) < 0 or
            i + di * (word_len - 1) >= self.size or
            j + dj * (word_len - 1) < 0 or
            j + dj * (word_len - 1) >= self.size
        ):
            return False

        for k in range(word_len):
            cell_value = self.grid[i + k * di][j + k * dj]
            if cell_value != ' ' and cell_value != word[k]:
                return False

        return True

    def _mark_word_in_direction(self, grid, word, i, j, direction):
        di, dj = self._get_direction_change(direction)
        for k in range(len(word)):
            grid[i + k * di][j + k * dj]['found'] = True

    def empty_words(self):
        self.words = []
