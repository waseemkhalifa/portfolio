use crate::deck::Card;

/* ----------------------- functions ----------------------- */
#[derive(Debug)]
pub struct Player {
    bank: i32,
    pub hand: Vec<Card>,
    bet: i32,
    hand_value: i32,
}

pub struct Dealer {
    hand: Vec<Card>,
    hand_value: i32,
}
