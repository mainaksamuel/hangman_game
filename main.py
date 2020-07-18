# Inspired by the Hangman game.
#
# Author: Samuel K.

import random
import urllib.request

game_options = {"nw": "guess a New Word", "qg": "Quit Game", "he": "show Help message", "sw": "show Secret Word"}


# Initialize the game.
def new_game(secret_word: str, number_of_tries: int, word_progress: str) -> list:
    secret_word = get_secret_word()
    word_progress = "".join(["_"] * len(secret_word))
    print("Guess the word: ", word_progress, end="\n")
    number_of_tries = 0
    return [secret_word, number_of_tries, word_progress]


# Verify User guess input is not zero or more than one character.
def valid_input(guess: str) -> bool:
    if len(guess) > 1 and guess not in game_options.keys():
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


# Generate random Secret Word
def get_secret_word() -> str:
    words_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    word_url_response = urllib.request.urlopen(words_url)
    word_url_response_text = word_url_response.read().decode()
    words = word_url_response_text.splitlines()
    new_secret_word = words[random.randint(0, len(words))]
    return new_secret_word


# Display the Help Message
def help_msg():
    print("Enter a command from list bellow")
    help_header = """Command:\tDescription:
--------\t------------"""
    print(help_header, end="\n")
    for key in game_options.keys():
        print("{}\t\t\t{}".format(key, game_options.get(key)), end="\n")


# Show at the end of each word play to allow the user to exit or continue playing the game.
def exit_option(secret_word="", number_of_tries=0, word_progress=""):
    option = input("New Game? [y/n]").strip().lower()
    if option == "y" or option == "yes":
        return new_game(secret_word, number_of_tries, word_progress)
    else:
        exit(0)


if __name__ == '__main__':

    # Display the welcome message on game start
    initial_message = """
                    Welcome to the Py-Hangman Game.
        For you to guess correctly, please enter one character at a time.
    """
    # Displayed when user guesses the secret word correctly.
    winning_message = """
            CONGRATULATIONS, YOU GUESSED CORRECTLY!!!
    """

    print(initial_message, end="\n")

    print("Enter `he` for help.")

    # Initialize the Secret word.
    secret_word = get_secret_word()

    # Generate blank/underscore placeholders for each character in secret word
    # The `word_progress` variable will track user progress in guessing the secret word correctly.
    word_progress = "".join(["_"] * len(secret_word))
    print("Guess the word: ", word_progress, end="\n")

    # Statistics to show user how many attempts they made before getting the correct secret word.
    number_of_tries = 0

    # Main game play
    while True:
        while completed(word_progress) is False:
            guess = input("Your Guess: ").strip().lower()
            while not valid_input(guess):
                print(word_progress)
                guess = input("Your Guess: ").strip().lower()

            # Affirm User Command
            if len(guess) > 1:
                user_affirmation = input("Do you want to {} ? [y/n]".format(game_options.get(guess))).strip().lower()
                if user_affirmation == "y" or user_affirmation == "yes":
                    if guess == "he":  # Show the Help Message
                        help_msg()
                    elif guess == "qg":  # Quit the Game
                        exit(0)
                    elif guess == "nw":  # Get a new Secret Word
                        secret_word, number_of_tries, word_progress = new_game(secret_word, number_of_tries,
                                                                               word_progress)
                        continue
                    elif guess == "sw":  # Show the Secret Word and give user option of continuing the game.
                        print("The Secret Word is '{}'; Number of tries = {}".format(secret_word, number_of_tries))
                        secret_word, number_of_tries, word_progress = exit_option()
                        continue
                    else:
                        pass
                else:
                    pass
                # Update number of tries to exclude help command entries
                number_of_tries -= 1

            # update user guess progress
            word_progress = update_progress(secret_word.lower(), guess, word_progress)
            print(word_progress)
            number_of_tries += 1

        print(winning_message,
              "Secret word = {};  Your guess = {}; Number of tries = {}; Word Length = {}".format(secret_word,
                                                                                                  word_progress,
                                                                                                  number_of_tries,
                                                                                                  len(secret_word)),
              end="\n")

        print("")
        # Allow the user to continue with the game after successfully guessing the secret word.
        secret_word, number_of_tries, word_progress = exit_option()

# TODO: Refactor to be more Object Oriented
