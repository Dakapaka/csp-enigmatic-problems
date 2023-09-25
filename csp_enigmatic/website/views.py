from flask import Blueprint, render_template, request, session, flash
import numpy as np
import website.sudoku as sd
from website.word_search import WordSearch
import random

views = Blueprint('views', __name__)

@views.route('/')
def home():
    sudoku = sd.Sudoku.sudoku_generator(0.5)
    words = []

    file = open('words/words.txt', 'r')
    for line in file:
        words.append(line.strip())
    file.close()

    for i in range(len(words)):
        words[i] = words[i].upper()

    wordSearch = WordSearch(10)
    random.shuffle(words)

    for word in words:
        wordSearch.add_word(word)
    return render_template(
        "home.html",
        sudoku=sudoku,
        word_search=wordSearch.generate()
    ) 

@views.route('/sudoku', methods=['GET', 'POST'])
def sudoku():
    if 'current_move_number' not in session:
        session['current_move_number'] = 1

    if request.method == 'POST':
        move_action = request.form.get('move_action')
        if move_action == 'previous':
            if session['current_move_number'] > 1:
                session['current_move_number'] -= 1
        elif move_action == 'next':
            if session['current_move_number'] < len(sd.Sudoku.sudoku_log):
                session['current_move_number'] += 1
            print(sd.Sudoku.coordinates_log[session['current_move_number']])
        elif move_action == 'solve':
            session['current_move_number'] = len(sd.Sudoku.sudoku_log)
        elif move_action == 'reset':
            session['current_move_number'] = 1
        elif move_action == 'generate':
            session['current_move_number'] = 1
            grid = sd.Sudoku.sudoku_generator(0.5)
            sd.Sudoku.solve(grid)
            sd.Sudoku.move_number += 1
            sd.Sudoku.sudoku_log[sd.Sudoku.move_number] = np.copy(grid)
    else:
        session['current_move_number'] = 1
        grid = sd.Sudoku.sudoku_generator(0.5)
        sd.Sudoku.solve(grid)
        sd.Sudoku.move_number += 1
        sd.Sudoku.sudoku_log[sd.Sudoku.move_number] = np.copy(grid)

    current_move_number = session['current_move_number']
    grid = sd.Sudoku.sudoku_log[current_move_number]
    return render_template(
        "sudoku.html",
        current_move_number=current_move_number,
        grid=grid, 
        move_number=sd.Sudoku.move_number, 
        move_log=sd.Sudoku.move_log,
        sudoku_log=sd.Sudoku.sudoku_log,
        coordinates_log=sd.Sudoku.coordinates_log
    )

@views.route('/word_search', methods=['GET', 'POST'])
def word_search():
    grid = None
    found_words = []

    if request.method == 'GET':
        session.clear()

    added_words = session.get('added_words', [])

    if request.method == 'POST':
        move_action = request.form.get('move_action')
        if move_action == 'generate':
            if len(added_words) >= 5:
                word_search = WordSearch(10)
                for word in added_words:
                    word_search.add_word(word)
                grid = word_search.generate()
                session['word_search_info'] = {
                    'grid': grid,
                    'words': word_search.words,
                }
            else:
                flash('Add at least 5 words before generating the grid.', 'warning')
        elif move_action == 'solve':
            word_search_info = session.get('word_search_info')

            if word_search_info:
                word_search = WordSearch(10)
                word_search.grid = word_search_info['grid']
                word_search.words = word_search_info['words']

                grid = word_search.solve()
                found_words = word_search.words

        elif move_action == 'add_word':
            new_word = request.form.get('new_word')
            if new_word:
                new_word = new_word.upper()
                added_words.append(new_word)
                session['added_words'] = added_words

        elif move_action == 'reset':
            session.clear()
            added_words = []

    if grid is None:
        word_search = WordSearch(10)
        grid = word_search.generate()
        session['word_search_info'] = {
            'grid': grid,
            'words': word_search.words,
        }

    return render_template(
        "word_search.html",
        grid=grid,
        found_words=found_words,
        added_words=added_words
    )

@views.route('/play_sudoku', methods=['GET', 'POST'])
def play_sudoku():
    message = ""
    if request.method == 'POST':
        move_action = request.form.get('move_action')
        if move_action == 'play':
            row = int(request.form.get('row')) - 1
            column = int(request.form.get('column')) - 1
            number = int(request.form.get('number'))
            solved = True

            solved_grid = np.array(session['grid'])
            sd.Sudoku.solve(solved_grid)
            if 0 <= row < 9 and 0 <= column < 9 and 1 <= number <= 9 and session['grid'][row][column] == 0:
                session['grid'][row][column] = number

            user_grid = np.array(session['grid'])
            if solved_grid[row][column] == user_grid[row][column]:
                for i in range(9):
                    for j in range(9):
                        if user_grid[i][j] == 0:
                            solved = False
                            break
                if solved:
                    message = 'Čestitke, riješili ste sudoku!'
                else:
                    message = 'Tačan potez!'
                    session['grid'] = user_grid.tolist()
            else:
                session['grid'][row][column] = 0
                message = 'Pogrešan potez!'

            added_words = session.get('added_words', [])

        elif move_action == 'solve':
            solved_grid = np.array(session['grid'])
            sd.Sudoku.solve(solved_grid)
            session['grid'] = solved_grid.tolist()
            message = 'Rješenje je prikazano.'
        
        elif move_action == 'generate':
            difficulty = request.form.get('difficulty')
            if difficulty == 'easy':
                fill_probability = random.uniform(0.7, 0.9)
            elif difficulty == 'medium':
                fill_probability = random.uniform(0.4, 0.6)
            elif difficulty == 'hard':
                fill_probability = random.uniform(0.2, 0.4)
            grid = sd.Sudoku.sudoku_generator(fill_probability)
            session['grid'] = grid.tolist()
            message = 'Novi sudoku je generisan.'

    if request.method == 'GET':
        grid = np.zeros((9, 9), dtype=int)
        session['grid'] = grid.tolist()
    else:
        grid = session['grid']

    return render_template(
        "play_sudoku.html",
        grid=grid,
        message=message
    )

@views.route('/play_word_search', methods=['GET', 'POST'])
def play_word_search():
    message = ""
    words = []
    grid = [{'letter': ' ', 'found': False} for i in range(10) for j in range(10)]
    
    if request.method == 'GET':
        session['found_words'] = []

    if 'found_words' not in session:
        session['found_words'] = []
    found_words = session['found_words']

    if 'guesses' not in session:
        session['guesses'] = {}
    guessed_words_coordinates = session.get('guesses', {})

    file = open('words/words.txt', 'r')
    for line in file:
        words.append(line.strip())
    file.close()

    for i in range(len(words)):
        words[i] = words[i].upper()

    wordSearch = WordSearch(10)
    random.shuffle(words)

    for word in words:
        wordSearch.add_word(word)

    guessed_words_coordinates = session.get('guesses', {})

    if request.method == 'POST':
        grid = session['word_search_info']['grid']
        wordSearch.grid = grid
        move_action = request.form.get('move_action')
        session['guesses'] = guessed_words_coordinates

        if move_action == 'play_word_search':
            start_row = int(request.form.get('row_start'))
            start_column = int(request.form.get('column_start'))
            end_row = int(request.form.get('row_end'))
            end_column = int(request.form.get('column_end'))

            valid_directions = [
                (0, 1), (1, 0), (1, 1), (0, -1),
                (-1, 0), (-1, -1), (-1, 1), (1, -1)
            ]

            for direction in valid_directions:
                i, j = start_row - 1, start_column - 1
                guessed_word = ""
                coordinates = []

                while 0 <= i < 10 and 0 <= j < 10:
                    guessed_word += wordSearch.grid[i][j]
                    coordinates.append((i, j))
                    i += direction[0]
                    j += direction[1]

                    if guessed_word in words:
                        if (end_row - 1 == i - direction[0] and end_column - 1 == j - direction[1]) or (i < 0 or i >= 10 or j < 0 or j >= 10):
                            for k in range(len(guessed_word)):
                                i -= direction[0]
                                j -= direction[1]
                            message = f"Čestitke! Pronašli ste riječ '{guessed_word}'."
                            found_words.append(guessed_word)
                            grid = wordSearch.grid
                            guessed_words_coordinates[guessed_word] = coordinates  # Store coordinates for the guessed word
                            session['guesses'] = guessed_words_coordinates
                            break

            if not message:
                message = "Nažalost, riječ nije validna."

    elif request.method == 'GET':
        session.clear()
        grid = wordSearch.generate()
        session['word_search_info'] = {
            'grid': grid,
            'words': wordSearch.words,
            'added_words': wordSearch.added_words
        }

    if len(found_words) == len(wordSearch.words):
        message = " Čestitke! Pronašli ste sve riječi!"

    session['found_words'] = found_words
    
    print(guessed_words_coordinates)
    return render_template(
        "play_word_search.html",
        message=message,
        grid=grid,
        found_words=found_words,
        added_words=session['word_search_info']['added_words'],
        guessed_words_coordinates=session.get('guesses', {})
    )
