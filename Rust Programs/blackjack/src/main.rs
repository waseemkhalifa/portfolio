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
use crate::user::User;

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
    deck.shuffle_deck();
    println!("{:?}", deck.deck);
    println!("");

    println!("{:?}", deck.hit());
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
    println!("");
    println!("");
    println!("");

    println!("{:?}", new_player.hand);
    println!("{:?}", new_player.hand[0].rank);
    println!("");
    new_player.hand_value = new_player.hand_value_calc(&new_player.hand); 
    println!("{}", new_player.hand_value);
    println!("");

    println!("{:?}", new_dealer.hand);
    println!("{:?}", new_dealer.hand[0].rank);
    println!("");
    new_dealer.hand_value = new_dealer.hand_value_calc(&new_dealer.hand); 
    println!("{}", new_dealer.hand_value);
    println!("");
    println!("");
    println!("");

    new_player.show_cards(&new_player.hand);
    println!("");
    println!("");

    new_dealer.show_cards(&new_dealer.hand);
    println!("");
    println!("");

    new_dealer.hidden_show_cards(&new_dealer.hand);
    new_dealer.hidden_hand_value = new_dealer.hidden_hand_value_calc(&new_dealer.hand); 
    println!("{}", new_dealer.hidden_hand_value);
    println!("");
    println!("");

    println!("bank: {}, bet: {}", new_player.bank, new_player.bet);
    new_player.make_bet(new_player.bank);
}
