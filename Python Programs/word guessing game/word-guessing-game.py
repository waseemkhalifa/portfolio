# ---------------------------------------------------------------------------                                                                           
# Text based word guessing game
# ---------------------------------------------------------------------------
# this is a simple text based word guessing game coded in python
# the game can be played via the terminal, using the following command 
# in the file location:
# python3 "filename.py"

# the concept of the game is as follows:
# the player starts the game with 10 points
# the player is asked how many letters of a word they would you like to 
# challenge themselves to
# the player is able to choose between 3-15 letters
# the word will be displayed with half of their letters missing randomly
# if the player solves the word, their points increase by the number of
# letters of the word they've solved
# if the player is unsuccessful in answering the word, their points are
# deducted by the number of letters in the word
# the player has up to 3 chances of solving the word

# we will import english words
from english_words import english_words_lower_set as words
# we will use this to pick words from random
import random
# for the floor method
import math
# this is the default number of points for the game (global variable)
points = 10

# this function will ask the player how many letters of a word they'd
# like to challenge themselves to
def letters():
  # accepted inputs
  # any number between 3 and 16
  # we'll convert the numbers in the list from int to string
  # as input is stored as a string (which we'll convert to int later)
  accepted_inputs = list(range(3, 16))
  accepted_inputs = [str(x) for x in accepted_inputs]
   # this original choice value can be anything that isn't an integer
  choice = 'wrong'
  # while the choice is not a digit, keep asking for input.
  while choice not in accepted_inputs:
    print('How many letters of a word would you like to challenge '+\
      'yourself to?')
    choice = input('Choose between 3 to 15: ')
    if choice not in accepted_inputs:
      print('')
      print('> Only numbers between 3 to 15 are valid inputs')
  print('')
  # we'll convert choice to int here
  choice = int(choice)
  return choice

# this function will pick a random word
# the word will have the length specified
def original_word(letters):
  word = [i for i in words if len(i) == letters and "'" not in i]
  word = random.choice(word)
  return word

# this function will hide half of the letters in the word by random
def hidden_word(orig_word):
  # work out len of orig_word and use floor
  hide = math.floor(len(orig_word)/2)
  orig_word = list(orig_word)
  lst = random.choices(orig_word, k=3)
  for i,x in enumerate(orig_word):
  return hide

hidden_word('')

orig_word = 'hello'
hide = math.floor(len(orig_word)/2)
orig_word = list(orig_word)
lst = random.choices(orig_word, k=hide)
