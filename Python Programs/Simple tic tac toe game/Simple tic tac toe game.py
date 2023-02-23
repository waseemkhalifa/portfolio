# This is a simple Create a Tic Tac Toe game, which can be played via the
# terminal, using the following command in the file location:
# python3 "Simple tic tac toe game.py"

# Info about the game:
  # > 2 players will be able to play the game 
      # (both sitting at the same computer)
  # > The board will be printed out every time a player makes a move
  # > You will be able to accept input of the player position which will then  
      # place a symbol on the board

                                                                      
# we'll create an empty board using numpy
import numpy as np

# this function will allow the user to choose the element in which they'd like
# to add their input
def choice():
    # this original choice value can be anything that isn't an integer
    choice = 'wrong'
    # while the choice is not a digit, keep asking for input.
    while choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        # we shouldn't convert here, otherwise we get an error on a wrong
        # input
        choice = input('Your Turn, choose an element: ')
        if choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print('Sorry, but you did not choose a valid element')
    # we can convert once the while loop above has confirmed we have a digit
    choice = int(choice)
    # this will match the element to the row & column of the array
    array_position = []
    if choice == 1:
        array_position = [0,0]
    elif choice == 2:
       array_position = [0,1]
    elif choice == 3:
       array_position = [0,2]
    elif choice == 4:
        array_position = [1,0]
    elif choice == 5:
       array_position = [1,1]
    elif choice == 6:
       array_position = [1,2]
    elif choice == 7:
       array_position = [2,0]
    elif choice == 8:
       array_position = [2,1]
    elif choice == 9:
       array_position = [2,2]
    return array_position

# this is for player_x
# this function replaces the board with the players input
def x_choice(board_display, element_choice):
    row_input = element_choice[0]
    col_input = element_choice[1]
    filled_element = ['X', 'O']
    while board_display[row_input][col_input] in filled_element:
        print('')
        print('There is already an input on the board, choose another element')
        element_choice = choice()
        row_input = element_choice[0]
        col_input = element_choice[1]
    board_display[row_input][col_input] = 'X'

# this is for player_o
# this function replaces the board with the players input
def o_choice(board_display, element_choice):
    row_input = element_choice[0]
    col_input = element_choice[1]
    filled_element = ['X', 'O']
    while board_display[row_input][col_input] in filled_element:
        print('')
        print('There is already an input on the board, choose another element')
        element_choice = choice()
        row_input = element_choice[0]
        col_input = element_choice[1]
    board_display[row_input][col_input] = 'O'

# this function will determine if a player has won
def won_game(board):
    # player X
    if board[0][0] == 'X' and board[0][1] == 'X' and board[0][2] == 'X':
        return True
    elif board[1][0] == 'X' and board[1][1] == 'X' and board[1][2] == 'X':
        return True
    elif board[2][0] == 'X' and board[2][1] == 'X' and board[2][2] == 'X':
        return True
    elif board[0][0] == 'X' and board[1][0] == 'X' and board[2][0] == 'X':
        return True
    elif board[0][1] == 'X' and board[1][1] == 'X' and board[2][1] == 'X':
        return True
    elif board[0][2] == 'X' and board[1][2] == 'X' and board[2][2] == 'X':
        return True
    elif board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X':
        return True
    elif board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X':
        return True
    # player O
    elif board[0][0] == 'O' and board[0][1] == 'O' and board[0][2] == 'O':
        return True
    elif board[1][0] == 'O' and board[1][1] == 'O' and board[1][2] == 'O':
        return True
    elif board[2][0] == 'O' and board[2][1] == 'O' and board[2][2] == 'O':
        return True
    elif board[0][0] == 'O' and board[1][0] == 'O' and board[2][0] == 'O':
        return True
    elif board[0][1] == 'O' and board[1][1] == 'O' and board[2][1] == 'O':
        return True
    elif board[0][2] == 'O' and board[1][2] == 'O' and board[2][2] == 'O':
        return True
    elif board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O':
        return True
    elif board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O':
        return True

# this is our game
def play_tic_tac_toe():
    # this will build our empty board 
    board = np.array([['1','2','3'],['4','5','6'],['7','8','9']])
    # this will be a counter of how many turns we've had in the game
    turns = 0
    # this is the max turns the game can have
    max_turns = 9
    # players in the game
    players = ['X', 'O']
    # while loop, to loop while the number of turns is less/equal to max_turns
    while turns < max_turns:
        # for loop for numbers of players
        for p in players:
            # we'll print the board at the start of every turn
            print('')
            print(board)
            print('')
            # break out of for loop if we've played all turns
            if turns == max_turns:
                print('')
                print('Nobody wins!')
                break
            elif turns > max_turns:
                break
            elif p == 'X':
                print('You are player X')
                # user inputs in which element they'd like their input
                element_choice = choice()
                # this will input the user's choice on the board
                # it will also take care of wrong inputs
                x_choice(board, element_choice)
                # we'll increment by one at the end of each turn
                turns+=1
                # check to see if player X has won
                if won_game(board) == True:
                    print('')
                    print(board)
                    print('')
                    print('Player X has won!')
                    turns = max_turns + 1
                    print('')
                    break
            # player O
            elif p == 'O':
                print('You are player O')
                # user inputs in which element they'd like their input
                element_choice = choice()
                # this will input the user's choice on the board
                # it will also take care of wrong inputs
                o_choice(board, element_choice)
                # we'll increment by one at the end of each turn
                turns+=1
                # check to see if player O has won
                if won_game(board) == True:
                    print('')
                    print(board)
                    print('')
                    print('Player O has won!')
                    print('')
                    turns = max_turns + 1
                    break

# to play the game
play_tic_tac_toe()