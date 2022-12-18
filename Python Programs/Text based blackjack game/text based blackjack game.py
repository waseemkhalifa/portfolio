# ---------------------------------------------------------------------------                                                                           
# Text based blackjack game
# ---------------------------------------------------------------------------                                                                         
# this is a simple text based blackjack game coded in python
# the game can be played via the terminal, using the following command 
# in the file location:
# python3 "filename.py"

# the player will be asked to bet from their bank (initially value of £100)
# the player will be shown two cards
# the dealers 1 card out of their two will be shown
# the player will be given a choice to hit or stand
# once the player stands, the dealer will continue to hit until their
# card value is above the players
# whoever gets closest to 21 wins
# whoever gets 21 wins (Blackjack)
# a draw will occur if both players have the same hand value
# whoever hits and their hand goes above 21, they go bust and the other
# player wins
# at the end of the round the players bank either increases or decreases
# based on their bet, and the outcome of the round (win or lose)
# at the end of each round the player can choose to continue playing
# or to quit

# this will be used to shuffle the deck
import random

# tuple of suits
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
# tuple of ranks
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 
  'Ten', 'Jack', 'Queen', 'King', 'Ace')
# dictionary of value to ranks, ace = 11 in this dictionary
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 
  'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
# dictionary of value to ranks, ace = 1 in this dictionary
values_2 = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 
  'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}

# card class
class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]
    self.value_2 = values_2[rank]
  def __str__(self):
    return self.rank + ' of ' + self.suit

# deck class
class Deck:
  def __init__(self):
    # note this only happens once upon creation of a new Deck
    # empty list where we will store the deck
    self.all_cards = []
    # we'll create a rank for each suit
    # this will be our deck
    for suit in suits:
      for rank in ranks:
        # this assumes the Card class has already been defined!
        self.all_cards.append(Card(suit, rank))
  # this will shuffle the deck
  def shuffle(self):
    # Note this doesn't return anything
    random.shuffle(self.all_cards)
  # this will give us the top card of our deck
  def hit(self):
    return self.all_cards.pop(0)
  # this will give the player/dealer the two cards at the start of the hand
  def intial_hand(self, created_player):
    a = 0
    while a != 2:
      created_player.append(self.hit())
      a+=1
    return created_player

# player's class
class Player:
  def __init__(self, bank=100, hand=[], bet=0, hand_value=[]):
    self.bank = bank
    self.hand = hand
    self.bet = bet
    self.hand_value = hand_value
  # method for the player to input their bet amount prior to the hand
  # the player can only bet from his bank holdings
  def make_bet(self):
    bet_input = False
    while bet_input == False:
      self.bet = int(input(f'Make a bet from your bank: £1 - £{self.bank}: '))
      if self.bet <= self.bank and self.bet > 0:
        bet_input = True
      else:
        print('Bet needs to be from your bank holdings')  
    return self.bet
  # this method calculates the players hand
  def hand_value_calc(self, hand):
    hand_value = []
    has_ace = False
    # we calculate the hand value
    # this is also a check to see if the hand has a Ace
    # in this for loop Ace will be considered 11 instead of 1
    for i, a in enumerate(hand):
      hand_value.append(hand[i].value)
      if hand[i].rank == 'Ace':
        has_ace = True
      else:
        continue
    # Ace will be considered 1 instead of 11, if the hand value is above 21
    if sum(hand_value) > 21 and has_ace == True:
      hand_value = []
      for i, a in enumerate(hand):
        hand_value.append(hand[i].value_2)
    return sum(hand_value)
  # method for the player to input if they'd like to hit or stand
  def hit_stand(self):
    print('Do you want to Hit or Stand?')
    choice = False
    while choice == False:
      players_choice = input('Choose one: Hit = 1 or Stand = 2: ')
      if players_choice in ['1', '2']:
        if players_choice == '1':
          players_choice = 'Hit'
          choice = True
        elif players_choice == '2':
          players_choice = 'Stand'
          choice = True
      else:
        print('Input only allows for 1 or 2')
    return players_choice
  # method to display the players hand/cards
  def cards_in_hand(self, hand):
    for i in range(len(hand)):
      print('', hand[i])
  # method to change bank value based on bet if the player won the hand
  def won_hand(self, bet):
    self.bet = bet
    self.bank = self.bank + self.bet
    print(f'Your bank now holds £{self.bank}')
  # method to change bank value based on bet if the player lost the hand
  def lost_hand(self, bet):
    self.bet = bet
    self.bank = self.bank - self.bet
    print(f'Your bank now holds £{self.bank}')

# dealer's class
class Dealer:
  def __init__(self, hand=[], hand_value=[]):
    self.hand = hand
    self.hand_value = hand_value
  # method to show the dealers hand value at the start of the round
  # we only show 1 of the two cards
  def initial_hand_value_calc(self, hand):
    return hand[1].value
  # method to show the dealers hand value
  def actual_hand_value_calc(self, hand):
    hand_value = []
    has_ace = False
    for i, a in enumerate(hand):
      hand_value.append(hand[i].value)
      if hand[i].rank == 'Ace':
        has_ace = True
      else:
        continue
    # if the hand contains an Ace and the hand value is above 21
    # ace will be considered as 1 instead of 11
    if sum(hand_value) > 21 and has_ace == True:
      hand_value = []
      for i, a in enumerate(hand):
        hand_value.append(hand[i].value_2)
    return sum(hand_value)
  # This will show 1 card and the other hidden at the start of the round
  def inital_cards_in_hand(self, hand):
    print('Dealer has the following hand:')
    print('-hidden card-')
    print('', hand[1])
  # this will show the dealers cards in their hand
  def actual_cards_in_hand(self, hand):
    print('Dealer has the following hand:')
    for i in range(len(hand)):
      print('', hand[i])

# this function is called when you want to play the game
def play_blackjack():
  # we'll a create a deck of cards
  # we'll also shuffle the deck
  deck = Deck()
  deck.shuffle()
  # welcome message to the game
  print('')
  print('Welcome to the Blackjack Game')
  print('')
  # we'll create the player
  player = Player()
  # we'll ask them how much they want to bet
  bet = player.make_bet()
  # we'll deal his initial hand
  player_hand = []
  player_hand = deck.intial_hand(player.hand)
  # we'll print the players hand
  print('')
  print('You have the following hand:')
  player.cards_in_hand(player_hand)
  # we'll get the value of the hand
  print('Value of your Hand:', player.hand_value_calc(player_hand))
  # we'll create the dealer
  dealer = Dealer()
  # we'll deal his initial hand
  dealer_hand = []
  dealer_hand = deck.intial_hand(dealer.hand)
  # we'll print the dealers initial hand
  print('')
  dealer.inital_cards_in_hand(dealer_hand)
  # we'll get the value of the dealers initial hand
  print('Value of Dealers Hand:', 
    dealer.initial_hand_value_calc(dealer_hand))
  # this will the main game
  print('')
  # 1 = continue to play the game, 2 = stop playing the game
  game_choice = '1'
  # if it's the first round, don't deal the cards again
  # else deal the cards again for the new round
  round = 1
  while game_choice == '1':
    # if it's the first round, don't deal the cards again
    # else deal the cards again for the new round
    if round != 1:
      print('')
      # we'll ask them how much they want to bet
      bet = player.make_bet()
      # we'll deal his initial hand
      player_hand = []
      player_hand = deck.intial_hand(player_hand)
      # we'll print the players hand
      print('')
      print('You have the following hand:')
      player.cards_in_hand(player_hand)
      # we'll get the value of the hand
      print('Value of your Hand:', player.hand_value_calc(player_hand))
      # we'll deal his initial hand
      dealer_hand = []
      dealer_hand = deck.intial_hand(dealer_hand)
      # we'll print the dealers initial hand
      print('')
      dealer.inital_cards_in_hand(dealer_hand)
      # we'll get the value of the dealers initial hand
      print('Value of Dealers Hand:', 
        dealer.initial_hand_value_calc(dealer_hand))
    game = True
    while game == True:
      # if the player has 21 in his initial hand
      if player.hand_value_calc(player_hand) == 21:
        print('Value of your Hand:', player.hand_value_calc(player_hand))
        print('')
        print('Blackjack! - You win this hand')
        player.won_hand(bet)
        game = False
        break
      # if the player/dealer doesn't have 21 in his initial hand
      else:
        # we ask the player if he wants to hit or stand
        print('')
        player_hit_stand = player.hit_stand()
        while player_hit_stand == 'Hit':
            print('')
            player_hand.append(deck.hit())
            print('You have the following hand:')
            player.cards_in_hand(player_hand)
            if player.hand_value_calc(player_hand) < 21:
              # we'll get the value of the hand
              print('')
              print('Value of your Hand:', player.hand_value_calc(player_hand))
              print('')
              player_hit_stand = player.hit_stand()
            elif player.hand_value_calc(player_hand) == 21:
              print('')
              print('Value of your Hand:', player.hand_value_calc(player_hand))
              print('')
              print('Blackjack! - You win this hand')
              print('')
              player.won_hand(bet)
              game = False
              break
            elif player.hand_value_calc(player_hand) > 21:
              print('')
              print('Value of your Hand:', player.hand_value_calc(player_hand))
              print('')
              print('Bust! - You lose this hand')
              print('')
              player.lost_hand(bet)
              game = False
              break
        if player_hit_stand == 'Stand':
          print('')
          dealer.actual_cards_in_hand(dealer_hand)
          # we'll get the actual value of the dealers initial hand
          print('Value of Dealers Hand:', 
          dealer.actual_hand_value_calc(dealer_hand))
          # dealer will continue to hit if their hand is below the players
          while dealer.actual_hand_value_calc(dealer_hand) < \
            player.hand_value_calc(player_hand):
            dealer_hand.append(deck.hit())
            print('')
            print('Dealer hit')
          # this is if both dealer & player have the same card value
          if dealer.actual_hand_value_calc(dealer_hand) == \
            player.hand_value_calc(player_hand):
            print('')
            dealer.actual_cards_in_hand(dealer_hand)
            # we'll get the actual value of the dealers hand
            print('Value of Dealers Hand:', 
            dealer.actual_hand_value_calc(dealer_hand))
            print('')
            print('You have the following hand:')
            player.cards_in_hand(player_hand)
            print('Value of your Hand:', player.hand_value_calc(player_hand))
            print('')
            print('Draw - Nobody Wins')
            game = False
            break
          # if the dealers card value is higher than the players
          # and it's below 21
          elif dealer.actual_hand_value_calc(dealer_hand) > \
            player.hand_value_calc(player_hand) \
            and dealer.actual_hand_value_calc(dealer_hand) < 21:
            print('')
            dealer.actual_cards_in_hand(dealer_hand)
            # we'll get the actual value of the dealers hand
            print('Value of Dealers Hand:', 
            dealer.actual_hand_value_calc(dealer_hand))
            print('')
            print('You have the following hand:')
            player.cards_in_hand(player_hand)
            print('Value of your Hand:', player.hand_value_calc(player_hand))
            print('')
            print('Dealer wins this hand')
            print('')
            player.lost_hand(bet)
            game = False
            break
          # if the dealers card value is higher than 21
          elif dealer.actual_hand_value_calc(dealer_hand) > 21:
            print('')
            dealer.actual_cards_in_hand(dealer_hand)
            print('')
            # we'll get the actual value of the dealers hand
            print('Value of Dealers Hand:', 
            dealer.actual_hand_value_calc(dealer_hand))
            print('')
            print('You have the following hand:')
            player.cards_in_hand(player_hand)
            print('Value of your Hand:', player.hand_value_calc(player_hand))
            print('')
            print('Dealer is bust! You win this hand')
            print('')
            player.won_hand(bet)
            game = False
            break
          # if the dealers gets blackjack
          elif dealer.actual_hand_value_calc(dealer_hand) == 21:
            print('')
            dealer.actual_cards_in_hand(dealer_hand)
            # we'll get the actual value of the dealers hand
            print('Value of Dealers Hand:', 
            dealer.actual_hand_value_calc(dealer_hand))
            print('')
            print('You have the following hand:')
            player.cards_in_hand(player_hand)
            print('Value of your Hand:', player.hand_value_calc(player_hand))
            print('')
            print('Blackjack! Dealer wins this hand')
            print('')
            player.lost_hand(bet)
            game = False
            break
    # if the player has no more money left in their bank
    if player.bank == 0:
      print('')
      print('You have no more money in the bank')
      print('GAME ENDS')
      game_choice = '2'
    # this ask's the player if they want to continue playing the game
    else:
      print('')
      for_loop_helper = True
      while for_loop_helper == True:
        game_choice = input('Continue Playing?: Yes = 1 or No = 2: ')
        if game_choice == '1':
          round = round + 1
          for_loop_helper = False
          break
        elif game_choice == '2':
          round = round + 1
          for_loop_helper = False
          print('')
          print('Thank you for playing - GOODBYE')
          break
        else:
          print('Input only allows for 1 or 2')

# play the backjack game
play_blackjack()