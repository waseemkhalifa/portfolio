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
use slowprint::slow_println;

/* ----------------------- functions ----------------------- */
// this will our main game function 
pub fn play_blackjack() {

    let delay = std::time::Duration::from_millis(30);

    println!("");
    slow_println("Welcome to the Blackjack Game", delay);
    println!("");

    let mut deck = create_deck();
    deck.shuffle_deck();

    let mut player = initialise_player(&mut deck);
    let mut dealer = initialise_dealer(&mut deck);

    // will be used in our game loop, if game_status == "Continue"
    // continue the game else end the game
    let mut game_status = GameStatus::Continue;

    // helper, if it's the first round we'll work out the intialised player
    // dealer card values. For subsequent rounds, we'll create a new deck
    // shuffle the cards and give fresh new cards to the player & dealer
    let mut game_round:i32 = 1;

    while game_status == GameStatus::Continue {

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

        let game_result:String;
        
        // if the player has 21 in his initial hand
        if player.hand_value == 21 && dealer.hand_value != 21 {
            println!("");
            slow_println("You have a blackjack!", delay);
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("YOU WIN!", delay);
            game_result = String::from("won");
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            println!("");
            slow_println("You have a blackjack!", delay);
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("The dealer also has a blackjack!", delay);
            slow_println("DRAW!", delay);
            game_result = String::from("draw");
        } else {
            game_result = game_result_calc(&mut player, &mut dealer, 
                &mut deck);
        }

        player.round_result(game_result);

        game_status = end_of_round(&mut player, &mut game_status);
        println!("{:?}", game_status);
        
        game_round+=1;
    }

}

// function to work out if the player/dealer has won the round
fn game_result_calc(player: &mut Player, dealer: &mut Dealer, 
        deck:&mut Deck) -> String {

    let delay = std::time::Duration::from_millis(30);

    let mut game_result = String::new();
    let mut player_choice = player.hit_stand();
    println!("");

    while player_choice == "Hit" {
        slow_println("You Hit!", delay);
        println!("");
        player.hand.push(deck.hit());
        player.hand_value = player.hand_value_calc(&player.hand);
        player.show_cards(&player.hand);
        player.show_hand_value(&player.hand_value);
        if player.hand_value == 21 && dealer.hand_value != 21 {
            slow_println("You have a blackjack!", delay);
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("YOU WIN!", delay);
            game_result = String::from("won");
            break
        } else if player.hand_value == 21 && dealer.hand_value == 21 {
            slow_println("You have a blackjack!", delay);
            println!("");
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("The dealer also has a blackjack!", delay);
            slow_println("DRAW!", delay);
            game_result = String::from("draw");
            break
        } else if player.hand_value >= 21 {
            println!("");
            slow_println("BUST!", delay);
            slow_println("YOU LOSE!", delay);
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
            slow_println("Dealer has a blackjack!", delay);
            slow_println("YOU LOSE!", delay);
            game_result = String::from("lost");
        }
        
        // dealer will continue to hit if their hand is below the players
        while dealer.hand_value < player.hand_value {
            dealer.hand.push(deck.hit());
            dealer.hand_value = dealer.hand_value_calc(&dealer.hand);
            slow_println("Dealer hit!", delay);
            println!("");
        }

        if dealer.hand_value == player.hand_value {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("DRAW!", delay);
            game_result = String::from("draw");
        } else if dealer.hand_value > player.hand_value 
                && dealer.hand_value < 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("YOU LOSE!", delay);
            game_result = String::from("lost");
        } else if dealer.hand_value > 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("DEALER IS BUST!", delay);
            slow_println("YOU WIN!", delay);
            game_result = String::from("won");
        } else if dealer.hand_value == 21 {
            dealer.show_cards(&dealer.hand);
            dealer.show_hand_value(&dealer.hand_value);
            println!("");
            slow_println("Dealer has a blackjack!", delay);
            slow_println("YOU LOSE!", delay);
            game_result = String::from("lost");
        }   
    }

    return game_result;
}

// function for end of round
fn end_of_round(player: &mut Player, game_status: &mut GameStatus) -> GameStatus {
    println!("");

    let delay = std::time::Duration::from_millis(30);

    if player.bank == 0 {
        slow_println("You have no more money in the bank", delay);
        slow_println("GAME ENDS - GOODBYE!", delay);
        println!("");
        let game_status = GameStatus::End;
    } else {
        // we'll create a hashmap to map int choice to string
        let mut hm_choice: HashMap<i32, GameStatus> = HashMap::new();
        hm_choice.insert(1, GameStatus::Continue);
        hm_choice.insert(2, GameStatus::End);

        // this is a loop, which will only end if a valid input is entered
        let choice = loop {
            slow_println("Continue Playing?: Yes = 1 or No = 2: ", delay);
            
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
                slow_println("Input not accepted!", delay);
                slow_println("Input only allows for 1 or 2", delay);
                continue;
            }

            // this will be printed if the value entered was not int
            println!("");
            slow_println("Input not accepted!", delay);
            slow_println("Input only allows for 1 or 2", delay);
        };

        let game_status_2 = hm_choice.get(&choice).unwrap();
        let game_status = *game_status_2;

        if game_status == GameStatus::End {
            println!("");
            slow_println("Thank you for playing", delay);
            slow_println("GOODBYE!", delay);
            println!("");
        }
    }
    
    return game_status;
}

// we will create an enum for game_status
#[derive(Debug, PartialEq, Copy, Clone)]
enum GameStatus {
    Continue,
    End
}