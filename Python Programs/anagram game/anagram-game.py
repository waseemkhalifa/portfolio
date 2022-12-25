# ---------------------------------------------------------------------------                                                                           
# Text based anagram game
# ---------------------------------------------------------------------------
# this is a simple text based anagram game coded in python
# the game can be played via the terminal, using the following command 
# in the file location:
# python3 "filename.py"

# the concept of the game is as follows:
# the player starts the game with 10 points
# the player is asked how many letters of a anagram would you like to challenge
# themselves to
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
# this is the default number of points for the game (global variable)
points = 10

# this function will ask the player how many letters of an anagram they'd
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
    print('How many letters of a anagram would you like to challenge '+\
      'yourself to?')
    choice = input('Choose between 3 to 15: ')
    if choice not in accepted_inputs:
      print('')
      print('Only numbers between 3 to 15 are valid inputs')
  # we'll convert choice to int here
  choice = int(choice)
  return choice

# this function will pick a random word
# the word will have the length specified
def original_word(letters):
  word = [i for i in words if len(i) == 5]
  word = random.choice(word)
  return word

# this function will shuffle the original_word
def shuffle_word(word):
  word = list(word)
  random.shuffle(word)
  word = ''.join(word)
  return word

# this function will ask the player to solve the anagram
# they will have a maximum of 3 attempts
# if they get it correct/not the function will print a message

a = original_word(3)
print(a)
shuffle_word(a)

a = [i for i in words if len(i) == 5]
a
b = random.choice(a)
print(b)
c = list(b)
print(c)
random.shuffle(c)

