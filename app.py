from flask import Flask, render_template, request, redirect, url_for
import random
import openai
import time
import json
import os
import unittest

#print(url_for('static', filename='style.css'))
app = Flask(__name__)


def generate_hint(word, guess):
    prompt = f"""You are an assistant in a word-guessing game where the user needs to guess a specific 5-letter word. The user has made a guess and you need to help them guess the correct word within three more attempts.

Please generate a hint based on the following information:
- The target word is '{word}'.
- The user's most recent guess is '{guess}'.

Your hint should:
1. Be a single sentence that describes the meaning of the {word} without making
it too simple for the user
2. Describe the meaning, characteristics, or usage of the target word without revealing the word itself.
2. Provide a clue that helps the user get closer to guessing the correct word by describing its context or attributes.
3. Do not give away the word or any letters directly.
4. Be clear enough to guide the user toward understanding the nature of the word.

Example hint: "If the word is broke - the hint could be having run out of money"
"""
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    hint = completion.choices[0].message.content.strip()
    return hint

class WordleGame:
    def __init__(self, answer_list_path, word_list_path):
        self.answer_list_path = answer_list_path
        self.word_list_path = word_list_path
        self.answer_list = self.read_words_from_file(answer_list_path)
        self.word_list = self.read_words_from_file(word_list_path)

    def read_words_from_file(self, file_path):
        """Read words from a file and return a list of words."""
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return []
        
        with open(file_path, 'r') as file:
            words = [line.strip().lower() for line in file if line.strip()]
        return words

    def pick_random_word(self):
        """Pick a random word from the answer list."""
        return random.choice(self.answer_list) if self.answer_list else None

    def is_valid_guess(self, guess):
        """Check if the guess is in the word list."""
        return guess in self.word_list

    def is_correct_length(self, guess, length=5):
        """Check if the guess has the correct length."""
        return len(guess) == length

    def get_board_state(self, guesses, target_word):
        """Get the board state based on guesses and target word."""
        board = []
        for guess in guesses:
            result = [
                f"<span style='color: green;'>{guess[i]}</span>" if guess[i] == target_word[i]
                else f"<span style='color: orange;'>{guess[i]}</span>" if guess[i] in target_word
                else f"<span>{guess[i]}</span>"
                for i in range(len(guess))
            ]
            board.append(" ".join(result))
        return board

    def save_score(self, username, target_word, time_taken, num_guesses, points):
        """Save the score to a JSON file."""
        score = {
            "username": username,
            "target_word": target_word,
            "time_taken": time_taken,
            "num_guesses": num_guesses,
            "points": points
        }
        try:
            with open('scores.json', 'r') as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
        scores.append(score)
        with open('scores.json', 'w') as file:
            json.dump(scores, file, indent=4)

    def get_hint(self, target_word, revealed_letters):
        """Get a hint for the target word."""
        for i, letter in enumerate(target_word):
            if i not in revealed_letters:
                revealed_letters.add(i)
                return i, letter
        return None, None

    def calculate_points(self, num_guesses, hints_used):
        """Calculate the points based on guesses and hints used."""
        max_points = 100
        deduction_per_guess = 5
        deduction_per_hint = 10
        points = max_points - (num_guesses - 1) * deduction_per_guess - hints_used * deduction_per_hint
        return max(0, points)

# Initialize game instance with file paths
game = WordleGame(
    answer_list_path='/Users/palakgupta/Desktop/Wordle V1/answerlist.txt',
    word_list_path='/Users/palakgupta/Desktop/Wordle V1/wordlist.txt'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    username = request.form['username']
    if len(username) < 16 and username.isalnum():
        return redirect(url_for('play_game', username=username))
    else:
        return redirect(url_for('home'))

@app.route('/play/<username>', methods=['GET', 'POST'])
def play_game(username):
    instructions = """
        <p><span style="color: red; font-weight: bold; text-transform: uppercase;">Welcome to Wordle!</span></p>
        <p><span style="font-weight: bold;">This is how the game goes:</span></p>
        <ul>
            <li>You have to guess a 5-letter word.</li>
            <li>You will have six attempts to do so, and your progress will be recorded.</li>
        </ul>
        <p><span style="font-weight: bold;">Hints:</span></p>
        <ul>
            <li>You can request hints after 3 attempts.</li>
            <li>Each hint will reveal one letter in the correct position.</li>
        </ul>
        <p><span style="font-weight: bold;">Points:</span></p>
        <ul>
            <li>You start with a maximum score.</li>
            <li>Points are deducted for each guess and hint used.</li>
        </ul>
        <p>Good luck!</p>
    """
    error = None

    if request.method == 'POST':
        target_word = request.form.get('target_word')
        guesses = request.form.get('guesses', '').split(',')
        revealed_letters = set(map(int, request.form.get('revealed_letters', '').split(','))) if request.form.get('revealed_letters') else set()
        hints_used = int(request.form.get('hints_used', 0))
        start_time = float(request.form.get('start_time', time.time()))
        attempts = int(request.form.get('attempts', 6))

        if 'hint' in request.form:
            if len(guesses) < 3:
                error = "You can only request hints after 3 attempts."
            elif hints_used > 0:
                error = "You can only request one hint per game."
            else:
                hint = generate_hint(target_word, guesses[-1])
                hints_used += 1
            
        else:
            guess = request.form.get('guess', '').lower().strip()
            
            if not guess:
                error = "Please enter a guess."
            elif not game.is_correct_length(guess):
                error = "Guess must be exactly 5 characters long."
            elif not game.is_valid_guess(guess):
                error = "Guess is not in the word list."
            elif guess in guesses:
                error = "You have already guessed that word."
            else:
                guesses.append(guess)
                attempts -= 1

                if guess == target_word:
                    time_taken = time.time() - start_time
                    num_guesses = len(guesses)
                    points = game.calculate_points(num_guesses, hints_used)
                    game.save_score(username, target_word, time_taken, num_guesses, points)
                    return render_template('win.html', target_word=target_word, time_taken=time_taken, num_guesses=num_guesses, points=points)
                
                if attempts <= 0:
                    return render_template('lose.html', target_word=target_word)

        board = game.get_board_state(guesses, target_word)
        return render_template('game.html', username=username, target_word=target_word, guesses=','.join(guesses), board=board, start_time=start_time, error=error, instructions=instructions, revealed_letters=','.join(map(str, revealed_letters)), hints_used=hints_used, attempts=attempts)
    
    target_word = game.pick_random_word()
    start_time = time.time()
    attempts = 6
    return render_template('game.html', username=username, target_word=target_word, guesses='', start_time=start_time, instructions=instructions, revealed_letters='', hints_used=0, attempts=attempts)

if __name__ == '__main__':
    app.run(debug=True)

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.game = WordleGame(
            answer_list_path='/path/to/answerlist.txt',
            word_list_path='/path/to/wordlist.txt'
        )
        self.target_word = 'apple'
        self.guesses = ['apple', 'crane', 'spend']
        self.revealed_letters = set()

    def test_is_valid_guess(self):
        self.assertTrue(self.game.is_valid_guess('crane'))
        self.assertFalse(self.game.is_valid_guess('crane123'))
        self.assertFalse(self.game.is_valid_guess('wrong'))


    def test_is_correct_length(self):
        self.assertTrue(self.game.is_correct_length('crane'))
        self.assertFalse(self.game.is_correct_length('applepie'))

    def test_get_board_state(self):
        expected_board = [
            '<span>a</span> <span>p</span> <span>p</span> <span>l</span> <span>e</span>',
            '<span>s</span> <span>p</span> <span>e</span> <span>n</span> <span>d</span>',
            '<span>c</span> <span>r</span> <span>a</span> <span>n</span> <span>e</span>',
        ]
        self.assertEqual(self.game.get_board_state(self.guesses, self.target_word), expected_board)

    def test_calculate_points(self):
        self.assertEqual(self.game.calculate_points(2, 0), 95)
        self.assertEqual(self.game.calculate_points(4, 2), 65)

if __name__ == '__main__':
    unittest.main()

