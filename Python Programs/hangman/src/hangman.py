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

    wrong_guess_counter = wrong_guess_counter - 1
    
    # these are the hangman stages
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
    stages = [stage_1, stage_2, stage_3, stage_4, stage_5, stage_6, stage_7]

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
        if guess == actual_word:
            return actual_word
        else:
            return currently_guessed_word
    # if the guess is one letter
    else:
        for acl_letter, crt_letter in zip(actual_word, currently_guessed_word):
            if acl_letter == guess:
                output_string += guess
            else:
                output_string += crt_letter
    return output_string


# ------------------------------------ main --------------------------------- #
word_list = import_words()
word = get_word(word_list)
word = clean_word(word)
word_dashed = dash_word(word)

print(word)
print(word_dashed)








