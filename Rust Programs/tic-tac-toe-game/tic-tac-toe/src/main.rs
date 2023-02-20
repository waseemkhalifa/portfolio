/* ----------------- Text based Tic Tac Toe game ------------- */
/*
    This is a simple text based tic tac toe game coded in Rust

    Info about the game:
    > 2 players will be able to play the game, both sitting at the same
    computer
    > The board will be printed out every time the player makes a move
    > The game accepts an input of the player's position which will then
    place a symbol on the board
*/

/* ----------------------- main ----------------------- */
fn main() {
    // this will build our empty board 
    let mut a = arr2(&[[1, 2, 3], [4, 5, 6], [7, 8, 9]]);
                   
    println!("{}", a);
}

/* ----------------------- packages ----------------------- */
// this will be used by the computer to choose rock paper scissors at random
use ndarray::arr2;

/* ----------------------- functions ----------------------- */
