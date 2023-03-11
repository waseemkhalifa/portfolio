/* ----------------------- imports ----------------------- */
use crate::deck::create_deck;
use crate::user::User;
use crate::user::initialise_dealer;
use crate::user::initialise_player;

/* ----------------------- functions ----------------------- */
/* this will our main game function */
pub fn game() {

    // welcome message to the game
    println!("");
    println!("Welcome to the Blackjack Game");
    println!("");

    // will be used in our game loop, if game_status == "Continue"
    // continue the game else end the game
    let mut game_status = String::from("Continue");

    while game_status == "Continue" {
        // we"ll initialise a deck and shuffle it
        let mut deck = create_deck();
        deck.shuffle_deck();

        // welcome message to the game
        println!("");
        println!("Welcome to the Blackjack Game");
        println!("");

        // we'll initialise the player
        let mut player = initialise_player(&mut deck);
        // work out their hand value
        player.hand_value = player.hand_value_calc(&player.hand);

        // we'll initialise the dealer and show their hand (one card hidden)
        let mut dealer = initialise_dealer(&mut deck);
        // work out their hand value
        dealer.hand_value = dealer.hand_value_calc(&dealer.hand);
        // work out their hidden hand value
        dealer.hidden_hand_value = dealer.hidden_hand_value_calc(&dealer.hand);

        // we'll ask the player to make a bet
        player.make_bet(player.bank);

        // we'll now show the dealers hand (with on card hidden)
        // we'll also show the value of the hand (with on card hidden)
        dealer.hidden_show_cards(&dealer.hand);
        dealer.show_hidden_hand_value(&player.hand_value);

        // we'll now show the players card in hand with their value
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);
        
        // ask the player if they want to hit or stand
        // player.hit_stand();

    }

}