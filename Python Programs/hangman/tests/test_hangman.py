import unittest

# ------------------------------------ functions --------------------------- #
# this function will replace the word with dashes
def dash_word(word):
    word_list = []
    for letter in range(0, len(word)):
        word_list.append("_")
    word_dashed = " ".join(word_list)
    return word_dashed


# this function will remove numbers and symbols
def clean_word(word):
    word = "".join(letter if letter.isalpha() else "" for letter in word)
    return word


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


# this function takes the user's guess input
def guess_input():
    input_value = False
    while input_value == False:
        guess = input("Guess a letter OR the correct word: ")
        if guess.isalpha() == False:
            print()
            print("Guess must not include numbers or symbols")
        else:
            input_value = True
    return guess

# ------------------------------------ tests --------------------------- #
class word_frequency_finder_tests(unittest.TestCase):

    # test for dash_word function
    def test_dash_word_hello(self):
        self.test_input = "hello"
        self.test_expected = "_ _ _ _ _"
        self.test_output = dash_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_dash_word_wave(self):
        self.test_input = "wave"
        self.test_expected = "_ _ _ _"
        self.test_output = dash_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)

    def test_dash_word_a(self):
        self.test_input = "a!"
        self.test_expected = "_ _"
        self.test_output = dash_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)


    # test for clean_word function
    def test_clean_word_hello(self):
        self.test_input = "he12314^^$!llo!!!"
        self.test_expected = "hello"
        self.test_output = clean_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_clean_word_wave(self):
        self.test_input = "!!!2214wav213e12312313""$%%%^^$££"
        self.test_expected = "wave"
        self.test_output = clean_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)

    def test_clean_word_a(self):
        self.test_input = "a!"
        self.test_expected = "a"
        self.test_output = clean_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)


    # test for hangman_stage function
    def test_hangman_stage_second(self):
        self.test_input = 2
        self.test_expected = """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """
        self.test_output = hangman_stage(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_hangman_stage_first(self):
        self.test_input = 1
        self.test_expected = """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
        self.test_output = hangman_stage(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)

    def test_hangman_stage_last(self):
        self.test_input = 7
        self.test_expected = """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """
        self.test_output = hangman_stage(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)


    # test for dash_word function
    def test_guess_outcome_1(self):
        self.actual_word = "hello"
        self.current_guessed = "_e__o"
        self.test_input = "l"
        self.test_expected = "_ello"
        self.test_output = guess_outcome(self.actual_word,
                                         self.current_guessed,
                                         self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_guess_outcome_2(self):
        self.actual_word = "hello"
        self.current_guessed = "he___"
        self.test_input = "l"
        self.test_expected = "hell_"
        self.test_output = guess_outcome(self.actual_word,
                                         self.current_guessed,
                                         self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_guess_outcome_3(self):
        self.actual_word = "hello"
        self.current_guessed = "he___"
        self.test_input = "hello"
        self.test_expected = "hello"
        self.test_output = guess_outcome(self.actual_word,
                                         self.current_guessed,
                                         self.test_input)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_guess_outcome_4(self):
        self.actual_word = "hello"
        self.current_guessed = "h____"
        self.test_input = "hello"
        self.test_expected = "hello"
        self.test_output = guess_outcome(self.actual_word,
                                         self.current_guessed,
                                         self.test_input)
        self.assertEqual(self.test_output, self.test_expected)

    def test_guess_outcome_5(self):
        self.actual_word = "hello"
        self.current_guessed = "h____"
        self.test_input = "mel"
        self.test_expected = "hello"
        self.test_output = guess_outcome(self.actual_word,
                                         self.current_guessed,
                                         self.test_input)
        self.assertNotEqual(self.test_output, self.test_expected)


    # test for guess_input function
    def test_guess_input_1(self):
        self.test_expected = "hello"
        self.test_output = guess_input()
        self.assertEqual(self.test_output, self.test_expected)
    
    # test for guess_input function
    def test_guess_input_2(self):
        self.test_expected = "h"
        self.test_output = guess_input()
        self.assertEqual(self.test_output, self.test_expected)

# ------------------------------------ main --------------------------- #
if __name__ == "__main__":
    unittest.main()
