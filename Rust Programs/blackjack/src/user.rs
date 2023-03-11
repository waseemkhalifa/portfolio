/* ----------------------- imports ----------------------- */
// key value pairs of card values
use std::collections::HashMap;
use crate::deck::Card;
use crate::deck::Deck;
use crate::deck::Ranks;
// this will allow the user to input their choice for the game
use std::io;

/* ----------------------- functions ----------------------- */
#[derive(Debug)]
pub struct Player {
    pub bank: i32,
    pub hand: Vec<Card>,
    pub bet: i32,
    pub hand_value: i32,
}

impl Player {
    pub fn make_bet(&self, bank: i32) -> i32 {
        // this is a loop, which will only end if a valid input is entered
        let choice = loop {
            println!("");
            println!("Make a bet from your bank: £1 - £{}", bank);
            
            // this is Rust's user input method
            let mut choice = String::new();
            io::stdin().read_line(&mut choice).unwrap();

            // if the value entered was int
            if let Ok(val) = choice.trim().parse::<i32>() {
                // choice = choice.trim().parse::<i32>();
                if val > 0 && val <= bank {
                    break val;
                } 
                // this will print if the value entered was not valid
                println!("");
                println!("Input not accepted!");
                println!("Bet needs to be from your bank holdings");
                continue;
            }

            // this will be printed if the value entered was not int
            println!("");
            println!("Input not accepted! - Only number inputs accepted");
            println!("Bet needs to be from your bank holdings");
        };

        return choice;
    }

    pub fn hit_stand(&self) -> String {
        // we'll create a hashmap to map int choice to string
        let mut hm_choice: HashMap<i32, String> = HashMap::new();
        hm_choice.insert(1, "Hit".to_string());
        hm_choice.insert(2, "Stand".to_string());

        // this is a loop, which will only end if a valid input is entered
        let choice = loop {
            println!("");
            println!("Do you want to Hit or Stand?");
            println!("Choose one: Hit = 1 or Stand = 2:");
            
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

        let choice = hm_choice.get(&choice).unwrap().to_string();

        return choice;
    }

    // pub fn round_result(
    //     &self, player: &Player, round_result: String) -> String {
        
    // }
}


#[derive(Debug)]
pub struct Dealer {
    pub hand: Vec<Card>,
    pub hand_value: i32,
    pub hidden_hand_value: i32,
}

impl Dealer {
    pub fn hidden_hand_value_calc(&self, hand: &Vec<Card>) -> i32 {
        let mut hand_map: HashMap<Ranks, i32> = HashMap::new();
        hand_map.insert(Ranks::Two, 2);
        hand_map.insert(Ranks::Three, 3);
        hand_map.insert(Ranks::Four, 4);
        hand_map.insert(Ranks::Five, 5);
        hand_map.insert(Ranks::Six, 6);
        hand_map.insert(Ranks::Seven, 7);
        hand_map.insert(Ranks::Eight, 8);
        hand_map.insert(Ranks::Nine, 9);
        hand_map.insert(Ranks::Ten, 10);
        hand_map.insert(Ranks::Jack, 10);
        hand_map.insert(Ranks::Queen, 10);
        hand_map.insert(Ranks::King, 10);
        hand_map.insert(Ranks::Ace, 11);

        return *hand_map.get(&hand[1].rank).unwrap();
    }

    pub fn hidden_show_cards(&self, hand: &Vec<Card>) {
        println!("Dealer has the following hand:");
        println!("> -hidden card-");
        println!("> {:?} of {:?}", hand[1].rank, hand[1].suit);
    }
}

pub trait User {
    fn hand_value_calc(&self, hand: &Vec<Card>) -> i32;
    fn show_cards(&self, hand: &Vec<Card>);
}

impl User for Player {
    fn hand_value_calc(&self, hand: &Vec<Card>) -> i32 {
        let mut hand_map: HashMap<Ranks, i32> = HashMap::new();
        hand_map.insert(Ranks::Two, 2);
        hand_map.insert(Ranks::Three, 3);
        hand_map.insert(Ranks::Four, 4);
        hand_map.insert(Ranks::Five, 5);
        hand_map.insert(Ranks::Six, 6);
        hand_map.insert(Ranks::Seven, 7);
        hand_map.insert(Ranks::Eight, 8);
        hand_map.insert(Ranks::Nine, 9);
        hand_map.insert(Ranks::Ten, 10);
        hand_map.insert(Ranks::Jack, 10);
        hand_map.insert(Ranks::Queen, 10);
        hand_map.insert(Ranks::King, 10);
        hand_map.insert(Ranks::Ace, 11);

        let mut hand_values:Vec<i32> = Vec::new();
        let mut hand_values_index:Vec<usize> = Vec::new();
        for (index, cards) in hand.iter().enumerate() {
            hand_values.push(*hand_map.get(&cards.rank).unwrap());
            if cards.rank == Ranks::Ace {
                hand_values_index.push(index);
            }
        }

        let mut hand_value_sum:i32 = hand_values.iter().sum();
        let mut hand_values_index_len = hand_values_index.len();
        while hand_value_sum > 21 && hand_values_index_len > 0 {
            for (index, element) in hand_values_index.iter().enumerate() {
                hand_values[*element] = 1;
                hand_value_sum = hand_values.iter().sum();
                hand_values_index_len-=1;
                if hand_value_sum <= 21 {
                    break;
                }
            }
        }

        return hand_value_sum;
    }

    fn show_cards(&self, hand: &Vec<Card>) {
        println!("You have the following hand:");
        for card in hand {
            println!("> {:?} of {:?}", card.rank, card.suit)
        }
    }
}

impl User for Dealer {
    fn hand_value_calc(&self, hand: &Vec<Card>) -> i32 {
        let mut hand_map: HashMap<Ranks, i32> = HashMap::new();
        hand_map.insert(Ranks::Two, 2);
        hand_map.insert(Ranks::Three, 3);
        hand_map.insert(Ranks::Four, 4);
        hand_map.insert(Ranks::Five, 5);
        hand_map.insert(Ranks::Six, 6);
        hand_map.insert(Ranks::Seven, 7);
        hand_map.insert(Ranks::Eight, 8);
        hand_map.insert(Ranks::Nine, 9);
        hand_map.insert(Ranks::Ten, 10);
        hand_map.insert(Ranks::Jack, 10);
        hand_map.insert(Ranks::Queen, 10);
        hand_map.insert(Ranks::King, 10);
        hand_map.insert(Ranks::Ace, 11);

        let mut hand_values:Vec<i32> = Vec::new();
        let mut hand_values_index:Vec<usize> = Vec::new();
        for (index, cards) in hand.iter().enumerate() {
            hand_values.push(*hand_map.get(&cards.rank).unwrap());
            if cards.rank == Ranks::Ace {
                hand_values_index.push(index);
            }
        }

        let mut hand_value_sum:i32 = hand_values.iter().sum();
        let mut hand_values_index_len = hand_values_index.len();
        while hand_value_sum > 21 && hand_values_index_len > 0 {
            for (index, element) in hand_values_index.iter().enumerate() {
                hand_values[*element] = 1;
                hand_value_sum = hand_values.iter().sum();
                hand_values_index_len-=1;
                if hand_value_sum <= 21 {
                    break;
                }
            }
        }

        return hand_value_sum;
    }

    fn show_cards(&self, hand: &Vec<Card>) {
        println!("The Dealer had the following hand:");
        for card in hand {
            println!("> {:?} of {:?}", card.rank, card.suit)
        }
    }
}

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
        hidden_hand_value: 0,
    }
}
