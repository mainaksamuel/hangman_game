# Inspired by the Hangman game.
#
# Author: Samuel K.

import urllib.request
import random


# Verify User guess input is not zero or more than one character.
def valid_input(guess: str) -> bool:
    if len(guess) > 1:
        print("You entered too many characters.")
        return False
    elif len(guess) < 1:
        print("Did you guess a character?")
        return False
    else:
        return True


# Replace underscore with Hint or Guessed word
def update_progress(guess_word: str, guess: str, word_progress: str) -> str:
    cursor = 0
    w_progress = list(word_progress)
    for c in guess_word:
        if (c == guess) and (w_progress[cursor] == "_"):
            w_progress[cursor] = guess
            break
        cursor += 1
    return "".join(w_progress)


# Check if User has guessed the secret word correctly and that there are no blank spaces.
def completed(w_progress: str) -> bool:
    status: bool = False
    if "_" not in w_progress:
        status = True

    return status


# Generate random Word
def get_random_word()->str:
    words_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    word_url_response = urllib.request.urlopen(words_url)
    word_url_response_text = word_url_response.read().decode()
    words = word_url_response_text.splitlines()
    new_secret_word = words[random.randint(0, len(words))]
    return new_secret_word


if __name__ == '__main__':
    # Display the welcome message on game start
    initial_message = """
                    Welcome to the Py-Hangman Game.
        Try to guess the correct word within the minimum number of tries allowed.
        For you to guess correctly, please enter one character at a time.
    """
    # Displayed when user gueeses the secret word correctly.
    winning_message = """
            CONGRATULATIONS, YOU GUESSED CORRECTLY!!!
    """

    print(initial_message, end="\n")

    # Initialize the Secret word.
    secret_word = get_random_word()
    print("Secret word: ", secret_word, end="\n")

    # Generate blank/underscore placeholders for each character in secret word
    # The `word_progress` variable will track user progress in guessing the secret word correctly.
    word_progress = "".join(["_"] * len(secret_word))

    # Statistics to show user how many attempts they made before getting the correct secret word.
    number_of_tries = 0

    # Main game play. Exit if user guesses word correctly.
    while completed(word_progress) is False:
        guess = input("Your Guess: ")
        while not valid_input(guess):
            print(word_progress)
            guess = input("Your Guess: ")

        word_progress = update_progress(secret_word.lower(), guess.lower(), word_progress)
        print(word_progress)
        number_of_tries += 1

    print(winning_message,
          "Secret word = {};  Your guess = {} ; Number of tries = {}".format(secret_word, word_progress,
                                                                             number_of_tries), end="\n")
