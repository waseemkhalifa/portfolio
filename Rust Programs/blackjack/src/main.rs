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

/* ----------------------- imports ----------------------- */
mod deck;
use deck::create_deck;
mod user;
use user::initialise_player;
use user::initialise_dealer;

/* ----------------------- main ----------------------- */
fn main() {
    
    let mut deck = create_deck();
    println!("");
    println!("print raw deck");
    println!("{:?}", deck);
    println!("");
    println!("print vec");
    println!("{:?}", deck.deck);
    println!("");
    println!("print one card");
    println!("{:?}", deck.deck[5]);
    println!("");
    println!("Deck Shuffled");
    // deck.shuffle_deck();
    println!("{:?}", deck.deck);
    println!("");

    // println!("{:?}", deck.hit());
    println!("");

    let mut new_player = initialise_player(&mut deck);
    println!("{:?}", new_player);
    println!("");

    println!("{:?}", deck.deck);
    println!("");

    let mut new_dealer = initialise_dealer(&mut deck);
    println!("{:?}", new_dealer);
    println!("");

    println!("{:?}", deck.deck);
    println!("");

    
    
    
    use crate::deck::Card;
    use crate::deck::Suits::Diamonds;
    use crate::deck::Ranks::Ace;
    println!("{:?}", new_player.hand);
    println!("{:?}", new_player.hand[0].rank);
    println!("");
    new_player.hand.push(Card{suit:Diamonds, rank:Ace});
    // new_player.hand.push(Card{suit:Diamonds, rank:Ace});
    // new_player.hand.push(Card{suit:Diamonds, rank:Ace});
    use std::collections::HashMap;
    use crate::deck::Ranks;
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
    
    let mut vec:Vec<i32> = Vec::new();
    let mut index_vec:Vec<usize> = Vec::new();
    for (index, cards) in new_player.hand.iter().enumerate() {
        println!("{:?} {}", cards.rank, hand_map.get(&cards.rank).unwrap());
        vec.push(*hand_map.get(&cards.rank).unwrap());
        if cards.rank == Ranks::Ace {
            index_vec.push(index);
        }
    }
    vec[1] = 0;
    vec[2] = 0;
    println!("Vector: {:?}", vec);
    println!("index_vec: {:?}", index_vec);
    let mut sum:i32 = vec.iter().sum();
    println!("the total sum is: {}", sum);
    println!("");
    let mut index_vec_len = index_vec.len();
    while sum > 21 && index_vec_len > 0 {
        for (index, element) in index_vec.iter().enumerate() {
            vec[*element] = 1;
            sum = vec.iter().sum();
            println!("the total sum is: {}", sum);
            index_vec_len-=1;
            if sum <= 21 {
                break;
            }
        }
    }
    println!("");
    println!("Vector: {:?}", vec);
    println!("index_vec: {:?}", index_vec);
    let mut sum:i32 = vec.iter().sum();
    println!("the total sum is: {}", sum);
}
