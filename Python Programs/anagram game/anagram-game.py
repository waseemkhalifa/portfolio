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
from english_words import english_words_lower_set as words
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

# this function will shuffle the original_word
def shuffle_word(word):
  word = list(word)
  shuffle_word = word.copy()
  while word == shuffle_word:
    random.shuffle(word)
  shuffle_word = ''.join(word)
  return shuffle_word

# this function will ask the player to solve the anagram
# they will have a maximum of 3 attempts
# if they get it correct/not the function will return a message
def solve(orig_word, shuf_word):
  print('')
  print('Can you solve this anagram: {a}'.format(a=shuf_word))
  print('You have a maximum of 3 attempts')
  print('')
  max_attempts=3
  current_attempt=1
  while max_attempts!=0:
    print('> Attempt {a}'.format(a=current_attempt))
    attempt = input('Enter your guess: ')
    if attempt == orig_word:
      message = 'correct'
      max_attempts = 0
      break
    else:
      print('Incorrect guess!')
      print('')
      message = 'wrong'
      current_attempt+=1
      max_attempts-=1
  return message

# this function will work out points
def points_calc(solved, orig_word):
  global points
  if solved == 'correct':
    points+=len(orig_word)
    print('You answered correctly - WELL DONE!')
    print('Your points will increase by {a}'.format(a=len(orig_word)))
    print('You now have {a} points'.format(a=points))
  else:
    points-=len(orig_word)
    print('You did not answer correctly - YOU LOSE!')
    print('The correct answer was: "{a}"'.format(a=orig_word))
    print('Your points will decrease by {a}'.format(a=len(orig_word)))
    print('You now have {a} points'.format(a=points))

# this is the main function of the game
def game():
  global points
  print('')
  print('> Welcome to the Anagram game')
  print('> The game is played as follows')
  print('> You start off with 10 points')
  print("> You pick the number of letters of the anagram you'd like to "+\
    "challenge yourself to solving")
  print('> You will have 3 attempts to solve the anagram')
  print('> If you successfully solve the anagram, your points will increase'+\
    ' by the number of letters of the anagram')
  print('> If after 3 unsuccessful attempts, the round ends and your '+\
    'points will decrease by the number of letters of the anagram')
  print('> At then of the round you can choose to continue or end the game')
  print('')
  print('You have {a} points'.format(a=points))
  # while loop: if true carry on playing otherwise end the game
  while points > 0:
    letters_input = letters()
    orig_word = original_word(letters_input)
    shuf_word = shuffle_word(orig_word)
    solved = solve(orig_word, shuf_word)
    points_calc(solved, orig_word)
    # ask the player if they'd like to carry on playing or not
    # if they don't have any points left the game ends automatically
    if points > 0:
      choice = 'wrong'
      while choice not in ['1', '2']:
        print('')
        choice = input('Continue playing?: Yes(1) or No(2): ')
        print('')
        if choice not in ['1', '2']:
          print('')
          print('Only 1 or 2 are valid inputs')
        elif choice == '2':
          points = 0
    else:
      print('You have no points!')
  print('Thank you for playing - GOODBYE')
  print('')

game()