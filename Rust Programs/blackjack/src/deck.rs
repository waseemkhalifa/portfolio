/* ----------------------- packages ----------------------- */
// this will be used by the computer to shuffle the deck
use rand::thread_rng;
use rand::seq::SliceRandom;
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

#[derive(Debug, EnumIter, Copy, Clone, Eq, Hash, PartialEq)]
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
    pub suit:Suits,
    pub rank:Ranks,
}

#[derive(Debug, Clone)]
pub struct Deck {
    pub deck:Vec<Card>,
}

impl Deck {
    pub fn shuffle_deck(&mut self) {
        self.deck.shuffle(&mut thread_rng());
        self.deck.shuffle(&mut thread_rng());
        self.deck.shuffle(&mut thread_rng());
    }
    pub fn hit(&mut self) -> Card {
        return self.deck.pop().unwrap();
    }
    pub fn intial_hand(&mut self) -> Vec<Card> {
        let mut intial_hand_cards:Vec<Card> = Vec::new();
        let mut a = 0;
        while a != 2 {
            intial_hand_cards.push(self.hit());
            a+=1;
        }
        return intial_hand_cards;
    }
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
