/* ----------------------- packages ----------------------- */
// this will be used by the computer to choose rock paper scissors at random
// use rand::Rng;
// this will store our rock, paper & scissors as key value pairs
// use std::collections::HashMap;
// this will allow the user to input their choice for the game
// use std::io;
// this will allow us to iterate over a Enum
use strum::IntoEnumIterator;
use strum_macros::EnumIter;

/* ----------------------- functions ----------------------- */
#[derive(Debug, EnumIter, Copy, Clone)]
pub enum Suits {
    Hearts, 
    Diamonds, 
    Spades, 
    Clubs,
}

#[derive(Debug, EnumIter, Copy, Clone)]
pub enum Ranks {
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
    Ace,
}

#[derive(Debug, Copy, Clone)]
pub struct Card {
    suit:Suits,
    rank:Ranks,
}

#[derive(Debug, Clone)]
pub struct Deck {
    pub deck:Vec<Card>,
}



// this will create our deck of cards
pub fn create_deck() -> Deck {
    let mut helper_deck:Vec<Card> = vec![];
    for suits in Suits::iter() {
        for ranks in Ranks::iter() {
            let card = Card{suit:suits, rank:ranks};
            helper_deck.push(card);
        }
    }
    let deck = Deck{deck:helper_deck};
    return deck;
}