/* ----------------- Text based blackjack game ------------- */

/*
    This is a simple text based blackjack game coded in rust. The game plays
    as follows:
    > the player will be asked to bet from their bank (initially value of £100)
    > the player will be shown two cards
    > the dealers 1 card out of their two will be shown
    > the player will be given a choice to hit or stand
    > once the player stands, the dealer will continue to hit until their
        card value is above the players
    > whoever gets closest to 21 wins
    > whoever gets 21 wins (Blackjack)
    > a draw will occur if both players have the same hand value
    > whoever hits and their hand goes above 21, they go bust and the other
        player wins
    > at the end of the round the players bank either increases or decreases
        based on their bet, and the outcome of the round (win or lose)
    > at the end of each round the player can choose to continue playing
        or to quit
*/

/* ----------------------- packages ----------------------- */
// this will be used by the computer to choose rock paper scissors at random
use rand::Rng;
// this will store our rock, paper & scissors as key value pairs
use std::collections::HashMap;
// this will allow the user to input their choice for the game
use std::io;
// this will allow us to iterate over a Enum
use strum::IntoEnumIterator;
use strum_macros::EnumIter;

/* ----------------------- main ----------------------- */
fn main() {
    let mut deck: Vec<Card>  = vec![];
    for suits in Suits::iter() {
        for ranks in Ranks::iter() {
            let a = suits;
            let b = ranks;
            let card = Card{suit:a, rank:b};
            deck.push(card);
        }
    }
    println!("{:?}", deck);
    println!("");
    println!("{:?}", deck[1]);


}

/* ----------------------- functions ----------------------- */
// the derive attribute makes the enum printable
#[derive(Debug, EnumIter, Copy, Clone)]
enum Suits {
    Hearts, 
    Diamonds, 
    Spades, 
    Clubs
}

// the derive attribute makes the enum printable
#[derive(Debug, EnumIter, Copy, Clone)]
enum Ranks {
    Two, 
    Three, 
    Four, 
    Five, 
    Six, 
    Seven, 
    Eight, 
    Nine, 
    Ten, 
    Jack, 
    Queen, 
    King, 
    Ace
}
#[derive(Debug, Copy, Clone)]
struct Card {
    suit:Suits,
    rank:Ranks
}

// impl Card {
//     fn deck(& self) -> Vec<&str> {
//         println!("hello");
//     }
// }


// create hashmap in a function, which can extract the value needed
// acting like a look up function