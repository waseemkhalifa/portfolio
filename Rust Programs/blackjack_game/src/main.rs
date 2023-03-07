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

}



