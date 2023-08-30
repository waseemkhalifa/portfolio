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
    stage_0 = """
                   
                """
    stage_1 = """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """

    stage_2 = """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """

    stage_3 = """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """

    stage_4 = """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """
    
    stage_5 = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """
    
    stage_6 = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """
    
    stage_7 = """
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
    actual_word = actual_word.replace(" ", "")
    currently_guessed_word = currently_guessed_word.replace(" ", "")
    # empty helper string
    output_string = ""
    
    # if the guess is a word (more than one letter)
    if len(guess) > 1:
        if guess == actual_word:
            return actual_word
        else:
            return currently_guessed_word
    # if the guess is one letter
    else:
        for acl_letter, crt_letter in zip(actual_word, currently_guessed_word):
            if acl_letter == guess:
                output_string += guess + " "
            else:
                output_string += crt_letter + " "
    return output_string


# this function takes the user's guess input
def guess_input():
    input_value = False
    while input_value == False:
        guess = input("Guess a letter OR the correct word: ")
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
    print("- THANKS FOR PLAYING THE HANGMAN GAME -")
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

    wrong_guess_counter = 0

    while wrong_guess_counter < 7:
        print(word_to_guess_dashed)

        guessed_input = guess_input()

        guess_attempt = guess_outcome(word_to_guess, 
                                      word_to_guess_dashed, 
                                      guessed_input)
        
        if guess_attempt == word_to_guess_dashed:
            wrong_guess_counter += 1
        elif guess_attempt == word_to_guess:
            wrong_guess_counter = 8
        
        word_to_guess_dashed = guess_attempt
        
        print(hangman_stage(wrong_guess_counter))

        # TO DO
        # if the user inputs the same letter again, flag instead of accepting input
    
    game_over()

# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    main()
