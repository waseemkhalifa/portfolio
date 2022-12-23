# ---------------------------------------------------------------------------                                                                           
# Text based rock paper scissors game
# ---------------------------------------------------------------------------
# this is a simple text based rock paper scissors game coded in python
# the game can be played via the terminal, using the following command 
# in the file location:
# python3 "filename.py"

# the concept of the game is very simple
# the player will be asked to choose one of rock paper scissors
# the computer will choose rock paper scissors at random
# depending on who wins the round, will get one point
# at the end of each round the player will be asked if they want to
# continue playing or not

# the rules of rock paper scissors is as follows:
# rock beats scissors, scissors beats paper, paper beats rock

# this will be used by the computer to choose rock paper scissors at random
import random

# we create a dictionary for the input choice
choice_dict = {1:'Rock', 2:'Paper', 3:'Scissors'}

# default scores for the players
# we'll first define the score variables (which are global)
player_score = 0
computer_score = 0  

# this function will ask the player for their choice
def player_choice():
  # this original choice value can be anything that isn't an integer
  choice = 'wrong'
  # while the choice is not a digit, keep asking for input.
  while choice not in ['1', '2', '3']:
    print('Choose one of the following:')
    choice = input('Rock(1), Paper(2) or Scissors(3): ')
    if choice not in ['1', '2', '3']:
      print('')
      print('Only 1, 2 or 3 are valid inputs')
  # we'll convert choice to int here
  choice = int(choice)
  player_chosen = choice_dict[choice]
  return player_chosen

# this function will have the computer's choice (at random)
def computer_choice():
  lst = [1,2,3]
  computer_random = random.choice(lst)
  computer_chosen = choice_dict[computer_random]
  return computer_chosen

# this will work out who has won or lost
def won_lost(player_chosen, computer_chosen):
  # if player and computer have the same choice
  if player_chosen == computer_chosen:
    return 'Draw'
  # player wins
  elif player_chosen == 'Rock' and computer_chosen == 'Scissors':
    return 'YOU WIN!'
  elif player_chosen == 'Paper' and computer_chosen == 'Rock':
    return 'YOU WIN!'
  elif player_chosen == 'Scissors' and computer_chosen == 'Paper':
    return 'YOU WIN!'
  # computer wins
  elif computer_chosen == 'Rock' and player_chosen == 'Scissors':
    return 'YOU LOSE!'
  elif computer_chosen == 'Paper' and player_chosen == 'Rock':
    return 'YOU LOSE!'
  elif computer_chosen == 'Scissors' and player_chosen == 'Paper':
    return 'YOU LOSE!'

# this function will keep of the score
def score_keeper(play_score, comp_score, round_result):
  global player_score
  global computer_score
  if round_result == 'YOU WIN!':
    player_score+=1
    print('SCORE:  Player={a}   Computer={b}'.\
      format(a = player_score, b = computer_score))
  elif round_result == 'YOU LOSE!':
    computer_score+=1
    print('SCORE:  Player={a}   Computer={b}'.\
      format(a = player_score, b = computer_score))
  else:
    print('SCORE:  Player={a}   Computer={b}'.\
      format(a = player_score, b = computer_score))

# this is the main game function
def game():
  # print out a welcome message
  print('')
  print('Welcome to the Rock, Paper, Scissors Game')
  print('')
  # while loop: if true carry on playing otherwise end the game
  play = True
  while play == True:
    # we'll ask for the players choice
    player = player_choice()
    # the computer's random choice
    computer = computer_choice()
    # we'll print the choices
    print('')
    print('Player:{a}   Computer:{b}'.format(a = player, b = computer))
    # we will get the result for the round
    result = won_lost(player, computer)
    print(result)
    # we will print the score
    score_keeper(player_score, computer_score, result)
    # ask the player if they'd like to carry on playing or not
    choice = 'wrong'
    while choice not in ['1', '2']:
      print('')
      choice = input('Continue playing?: Yes(1) or No(2): ')
      print('')
      if choice not in ['1', '2']:
        print('')
        print('Only 1 or 2 are valid inputs')
      elif choice == '2':
        play = False

# this will start the game
game()