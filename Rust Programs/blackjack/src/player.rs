/* ----------------------- imports ----------------------- */
use crate::deck::Card;
use crate::deck::Deck;

/* ----------------------- functions ----------------------- */
#[derive(Debug)]
pub struct Player {
    pub bank: i32,
    pub hand: Vec<Card>,
    pub bet: i32,
    pub hand_value: i32,
}

#[derive(Debug)]
pub struct Dealer {
    pub hand: Vec<Card>,
    pub hand_value: i32,
}

pub trait User {
    fn initialise_player(&self, deck:&mut Deck) -> Player;
}

impl User for Player {
    fn initialise_player(&self, deck:&mut Deck) -> Player {
        Player {
            bank: 100,
            hand: deck.intial_hand(),
            bet: 0,
            hand_value: 0,
        }
    }
}