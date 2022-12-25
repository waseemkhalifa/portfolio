# ---------------------------------------------------------------------------                                                                           
# Text based anagram game
# ---------------------------------------------------------------------------
# this is a simple text based anagram game coded in python
# the game can be played via the terminal, using the following command 
# in the file location:
# python3 "filename.py"

# the concept of the game is as follows:
# the player starts the game with 10 points
# the player is asked how many letters of the anagram challenge they would like
# the player is able to choose between 3-15 letters
# if the player solves the anagram, their points increase by the number of
# letters of the anagram they've solved
# if the player is unsuccessful in answering the anagram, their points are
# deducted by the number of letters in the anagram
# the player has up to 3 chances of solving the anagram

# we will import english words
from english_words import english_words_lower_alpha_set as words
# we will use this to pick words from random
import random

a = [i for i in words if len(i) == 5]
a
random.choice(a)