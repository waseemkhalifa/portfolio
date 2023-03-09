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

// pub trait User {
//     fn hand_value_calc(&self, Vec<Card>) -> i32;
//     fn show_cards(&self, Vec<Card>);
// }

// impl User for Player {
//     fn hand_value_calc(&self, Vec<Card>) -> i32 {
//         let mut hand_value_map: HashMap<i32, String> = HashMap::new();
//         hm_choice.insert(1, "Rock".to_string());
//         hm_choice.insert(2, "Paper".to_string());
//         hm_choice.insert(3, "Scissors".to_string());
//     }
// }

// this will initialise our Player
pub fn initialise_player(deck:&mut Deck) -> Player {
    Player {
        bank: 100,
        hand: deck.intial_hand(),
        bet: 0,
        hand_value: 0,
    }
}

// this will initialise our Dealer
pub fn initialise_dealer(deck:&mut Deck) -> Dealer {
    Dealer {
        hand: deck.intial_hand(),
        hand_value: 0,
    }
}