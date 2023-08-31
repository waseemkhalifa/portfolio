# ------------------------------------ imports ----------------------------- #
import random

# ------------------------------------ functions --------------------------- #

# this function will import the word file as a list
def import_words():
    with open("words.txt", "r") as words:
        imported_words = []
        for word in words:
            word = word.strip()
            word = word.split()
            for x in word:
                imported_words.append(x)
    return imported_words


# this function will return a word for the player to guess
def get_word(words_list):
    word = random.choice(words_list)
    return word


# this function will remove numbers and symbols
def clean_word(word):
    word = "".join(letter if letter.isalpha() else "" for letter in word)
    return word


# this function will replace the word with dashes
def dash_word(word):
    word_list = []
    for letter in range(0, len(word)):
        word_list.append("_")
    word_dashed = " ".join(word_list)
    return word_dashed


# this function will return the hangman hangman_stage
def hangman_stage(wrong_guess_counter):
    
    # these are the hangman stages
    stage_7 = """
                   
                """
    stage_6 = """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """

    stage_5 = """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """

    stage_4 = """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """

    stage_3 = """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """
    
    stage_2 = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """
    
    stage_1 = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """
    
    stage_0 = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """

    # we'll store the hangman stages in a list
    stages = [stage_0, stage_1, stage_2, stage_3, stage_4, stage_5, stage_6, 
              stage_7]

    return stages[wrong_guess_counter]


# this function will do the following:
    # if the correct word is guessed, it'll return the un-dashed word
    # if the correct letter is guessed, it'll un-dash letters in the word
    # if in-correct, word will be left un-dashed
def guess_outcome(actual_word, currently_guessed_word, guess):
    # empty helper string
    output_string = ""
    
    # if the guess is a word (more than one letter)
    if len(guess) > 1:
        if guess == actual_word.replace(" ", ""):
            return actual_word
        else:
            return currently_guessed_word
    # if the guess is one letter
    else:
        for acl_ltr, crt_ltr in zip(actual_word.replace(" ", ""), 
                                          currently_guessed_word.replace(" ", "")):
            if acl_ltr == guess:
                output_string += guess + " "
            else:
                output_string += crt_ltr + " "
    return output_string


# this function takes the user's guess input
def guess_input():
    input_value = False
    while input_value == False:
        guess = input("Guess a letter OR the correct word: ")
        guess = guess.lower()
        # we'll continue asking the user for a guess if guess contains numbers 
        # or symbols
        if guess.isalpha() == False:
            print()
            print("INVALID INPUT!")
            print("Guess must not include numbers or symbols")
        else:
            input_value = True
    return guess


# this is our welcome message for the game
def intro():
    print()
    print("- WELCOME TO THE HANGMAN GAME -")
    print()
    print("- To win, simply guess the dashed word")
    print("- You can either input a letter at a time or guess the word")
    print("- If after 7 attempts, the correct word is not guessed...")
    print("HANGMAN!")
    print()


# this is our end message for the game
def game_over():
    print()
    print("- GAME OVER -")
    print()

    input_value = False
    while input_value == False:
        input_choice = input("Would you like to play again? (Y or N): ")
        input_choice = input_choice.upper()
        if input_choice in ["Y", "N"]:
            if input_choice == "Y":
                reset_counter = 7
                input_value = True
            elif input_choice == "N":
                reset_counter = 0
                input_value = True
        else:
            print('Input only allows for Y or N')
    return reset_counter


def correct_word(word):
    print("The correct word was: " + word)


# this is our welcome message for the game
def outro():
    print()
    print("- THANKS FOR PLAYING THE HANGMAN GAME -")
    print()
    print("- GOODBYE -")
    print()

# ------------------------------------ main --------------------------------- #
# this the main game function
def main():
    # our game intro
    intro()

    # we'll import the word list
    words_list = import_words()

    # we'll get a random word from the word list
    word_to_guess = get_word(words_list)

    # we'll clean the word of any numbers of symbols
    word_to_guess = clean_word(word_to_guess)

    # we'll dash the word
    word_to_guess_dashed = dash_word(word_to_guess)

    print("Guess the following word")

    wrong_guess_counter = 7

    while wrong_guess_counter > 0:
        print(word_to_guess_dashed)
        print()

        guessed_input = guess_input()

        guess_attempt = guess_outcome(word_to_guess, 
                                      word_to_guess_dashed, 
                                      guessed_input)
        
        if guess_attempt.replace(" ", "") == word_to_guess_dashed.replace(" ", ""):
            wrong_guess_counter -= 1
        elif guess_attempt.replace(" ", "") == word_to_guess.replace(" ", ""):
            break
        
        word_to_guess_dashed = guess_attempt
        
        print(hangman_stage(wrong_guess_counter))

        # TO DO
        # if the user inputs the same letter again, flag instead of accepting input
        # win/lose message
        # make every input lower case
    
    # show the correct word
    correct_word(word_to_guess)

    game_over()

    outro()

# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
