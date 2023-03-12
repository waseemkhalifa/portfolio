/* ----------------------- imports ----------------------- */
use crate::deck::create_deck;
use crate::user::User;
use crate::user::initialise_dealer;
use crate::user::initialise_player;
use crate::user::Player;
use crate::user::Dealer;
use crate::deck::Deck;
use std::collections::HashMap;
// this will allow the user to input their choice for the game
use std::io;

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
        player.make_bet();
        println!("");

        // we'll now show the dealers hand (with on card hidden)
        // we'll also show the value of the hand (with on card hidden)
        dealer.hidden_show_cards(&dealer.hand);
        dealer.show_hidden_hand_value(&dealer.hidden_hand_value);
        println!("");

        // we'll now show the players card in hand with their value
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);

        let mut game_result = String::new();
        
        // if the player has 21 in his initial hand
        if player.hand_value == 21 && dealer.hand_value != 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("YOU WIN!");
            game_result = String::from("won");
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            println!("");
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("The dealer also has a blackjack!");
            println!("DRAW!");
            game_result = String::from("draw");
        } else {
            game_result = game_result_calc(&mut player, &mut dealer, 
                &mut deck);
        }

        player.round_result(game_result);

        game_status = end_of_round(&mut player, &mut game_status);
        
        game_round+=1;
    }

}

// function to work out if the player/dealer has won the round
fn game_result_calc(player: &mut Player, dealer: &mut Dealer, 
        deck:&mut Deck) -> String {
    
    let mut game_result = String::new();
    let mut player_choice = player.hit_stand();
    println!("");

    while player_choice == "Hit" {
        player.hand.push(deck.hit());
        player.hand_value = player.hand_value_calc(&player.hand);
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);
        if player.hand_value == 21 && dealer.hand_value != 21 {
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("YOU WIN!");
            game_result = String::from("won");
            break
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            println!("You have a blackjack!");
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("The dealer also has a blackjack!");
            println!("DRAW!");
            game_result = String::from("draw");
            break
        } else if player.hand_value >= 21 {
            println!("");
            println!("BUST!");
            println!("YOU LOSE!");
            game_result = String::from("lost");
            break
        } else {
            println!("");
            player_choice = player.hit_stand();
        }
    }

    if player_choice == "Stand" {
        println!("");
        if dealer.hand_value == 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("Dealer has a blackjack!");
            println!("YOU LOSE!");
            game_result = String::from("lost");
        }
        
        // dealer will continue to hit if their hand is below the players
        while dealer.hand_value < player.hand_value {
            dealer.hand.push(deck.hit());
            dealer.hand_value = dealer.hand_value_calc(&dealer.hand);
            println!("Dealer hit!");
            println!("");
        }

        if dealer.hand_value == player.hand_value {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("DRAW!");
            game_result = String::from("draw");
        } else if dealer.hand_value > player.hand_value 
                && dealer.hand_value < 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("YOU LOSE!");
            game_result = String::from("lost");
        } else if dealer.hand_value > 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("DEALER IS BUST!");
            println!("YOU WIN!");
            game_result = String::from("won");
        } else if dealer.hand_value == 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            println!("Dealer has a blackjack!");
            println!("YOU LOSE!");
            game_result = String::from("lost");
        }   
    }

    return game_result;
}

// function for end of round
fn end_of_round(player: &mut Player, game_status: &mut String) -> String {
    println!("");

    if player.bank == 0 {
        println!("You have no more money in the bank");
        println!("GAME ENDS - GOODBYE!");
        println!("");
        *game_status = String::from("End");
    } else {
        // we'll create a hashmap to map int choice to string
        let mut hm_choice: HashMap<i32, String> = HashMap::new();
        hm_choice.insert(1, "Continue".to_string());
        hm_choice.insert(2, "End".to_string());

        // this is a loop, which will only end if a valid input is entered
        let choice = loop {
            println!("Continue Playing?: Yes = 1 or No = 2: ");
            
            // this is Rust's user input method
            let mut choice = String::new();
            io::stdin().read_line(&mut choice).unwrap();

            // if the value entered was int
            if let Ok(val) = choice.trim().parse::<i32>() {
                // choice = choice.trim().parse::<i32>();
                if val == 1 || val == 2 {
                    break val;
                } 
                // this will print if the value entered was not valid
                println!("");
                println!("Input not accepted!");
                println!("Input only allows for 1 or 2");
                continue;
            }

            // this will be printed if the value entered was not int
            println!("");
            println!("Input not accepted!");
            println!("Input only allows for 1 or 2");
        };

        *game_status = hm_choice.get(&choice).unwrap().to_string();
    }
    
    return game_status.to_string();
}