/* ----------------------- imports ----------------------- */
use crate::deck::create_deck;
use crate::user::User;
use crate::user::initialise_dealer;
use crate::user::initialise_player;

/* ----------------------- functions ----------------------- */
// this will our main game function 
pub fn play_blackjack() {

    println!("");
    println!("Welcome to the Blackjack Game");
    println!("");

    let mut deck = create_deck();
    deck.shuffle_deck();

    let mut player = initialise_player(&mut deck);
    let mut dealer = initialise_dealer(&mut deck);

    // will be used in our game loop, if game_status == "Continue"
    // continue the game else end the game
    let mut game_status = String::from("Continue");

    // helper, if it's the first round we'll work out the intialised player
    // dealer card values. For subsequent rounds, we'll create a new deck
    // shuffle the cards and give fresh new cards to the player & dealer
    let mut game_round:i32 = 1;

    while game_status == "Continue" {

        if game_round == 1 {
            player.hand_value = player.hand_value_calc(&player.hand);
            dealer.hand_value = dealer.hand_value_calc(&dealer.hand);
            dealer.hidden_hand_value = dealer
                .hidden_hand_value_calc(&dealer.hand);
        } else {
            deck = create_deck();
            deck.shuffle_deck();

            player.hand = deck.intial_hand();
            player.hand_value = player.hand_value_calc(&player.hand);

            dealer.hand = deck.intial_hand();
            dealer.hand_value = dealer.hand_value_calc(&dealer.hand);
            dealer.hidden_hand_value = dealer
                .hidden_hand_value_calc(&dealer.hand);
        }

        // we'll ask the player to make a bet
        player.make_bet(player.bank);
        println!("");

        // we'll now show the dealers hand (with on card hidden)
        // we'll also show the value of the hand (with on card hidden)
        dealer.hidden_show_cards(&dealer.hand);
        dealer.show_hidden_hand_value(&dealer.hidden_hand_value);
        println!("");

        // we'll now show the players card in hand with their value
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);

        let mut game_result = String::from("draw");
        
        // if the player has 21 in his initial hand
        if player.hand_value == 21 && dealer.hand_value != 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(dealer.hand);
            dealer.show_hand_value(dealer.hand_value);
            println!("");
            println!("YOU WIN!");
            game_result = String::from("won");
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(dealer.hand);
            dealer.show_hand_value(dealer.hand_value);
            println!("");
            println!("The dealer also has a blackjack!");
            println!("DRAW!");
            game_result = String::from("draw");
        } else {
            game_result = game_result_calc(player, dealer);
        }

        game_round+=1;
    }

}

// function to work out if the player/dealer has won the round
fn game_result_calc(player: Player, dealer: Dealer) -> String {
    println!("");
    let mut player_choice = player.hit_stand();
    println!("");

    while player_choice == "Hit" {
        player.hand.push(deck.hit());
        player.hand_value = player.hand_value_calc(&player.hand);
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);
        println!("");
        if player.hand_value == 21 && dealer.hand_value != 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(dealer.hand);
            dealer.show_hand_value(dealer.hand_value);
            println!("");
            println!("YOU WIN!");
            game_result = String::from("won");
            break
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(dealer.hand);
            dealer.show_hand_value(dealer.hand_value);
            println!("");
            println!("The dealer also has a blackjack!");
            println!("DRAW!");
            game_result = String::from("draw");
        } else if player.hand_value >= 21 {
            println!("");
            println!("BUST!");
            println!("YOU LOSE!");
            game_result = String::from("lost");
        }
    }

    if player_choice == "Stand" {
        println!("");
        dealer.show_cards(dealer.hand);
        dealer.show_hand_value(dealer.hand_value);
        if dealer.hand_value == 21 {
            println!("");
            println!("Dealer has a blackjack!");
            println!("YOU LOSE!");
            game_result = String::from("lost");
            break
        }
    }
}