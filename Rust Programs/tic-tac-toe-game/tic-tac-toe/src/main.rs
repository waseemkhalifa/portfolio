/* ----------------- Text based Tic Tac Toe game ------------- */
/*
    This is a simple text based tic tac toe game coded in Rust

    Info about the game:
    > 2 players will be able to play the game, both sitting at the same
    computer
    > The board will be println!ed out every time the player makes a move
    > The game accepts an input of the player"s position which will then
    place a symbol on the board
*/

/* ----------------------- main ----------------------- */
fn main() {
    // this will build our empty board 
    let mut board = arr2(&[[1, 2, 3], [4, 5, 6], [7, 8, 9]]);
    // this will be a counter of how many turns we"ve had in the game
    let mut turns = 0;
    // this is the max turns the game can have
    let max_turns = 9;
    // players in the game
    let players = ["x", "o"];
    // while loop, to loop while the number of turns is less/equal to max_turns
    while turns < max_turns {
        // for loop for numbers of players
        for p in players:
            // we"ll println! the board at the start of every turn
            println!("{}", board);
            // break out of for loop if we"ve played all turns
            if turns == max_turns {
                println!("Nobody wins!");
                break;
            } else if turns > max_turns {
                break;
            } else if p == "x" {
                println!("You are player x");
                // user inputs in which element they"d like their input
                element_choice = choice();
                // this will input the user"s choice on the board
                // it will also take care of wrong inputs
                x_choice(board, element_choice);
                // we"ll increment by one at the end of each turn
                turns+=1;
                // check to see if player x has won
                if won_game(board) == True {
                    println!("Player X has won!");
                    println!(board);
                    turns = max_turns + 1;
                    break;
                }
            }
            // player o
            else if p == "o" {
                println!("You are player o");
                // user inputs in which element they"d like their input
                element_choice = choice();
                // this will input the user"s choice on the board
                // it will also take care of wrong inputs
                o_choice(board, element_choice);
                // we"ll increment by one at the end of each turn
                turns+=1;
                // check to see if player o has won
                if won_game(board) == True {
                    println!("Player O has won!");
                    println!(board);
                    turns = max_turns + 1;
                    break;
                }
            }
    }
}

/* ----------------------- packages ----------------------- */
// this will be used by the computer to choose rock paper scissors at random
use ndarray::arr2;

/* ----------------------- functions ----------------------- */
// this function will allow the user to choose the element in which they"d like
// to add their input
def choice():
    // the only values we'll accept for our user input
    let correct_input: [i32; 9] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];

    // while the choice is not a digit, keep asking for input.
    while choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        // we shouldn't convert here, otherwise we get an error on a wrong
        // input
        choice = input('Your Turn, choose an element: ');
        if choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            print('Sorry, but you did not choose a valid element')
    // we can convert once the while loop above has confirmed we have a digit
    choice = int(choice)
    // this will match the element to the row & column of the array
    array_position = []
    if choice == 1:
        array_position = [0,0];
    elif choice == 2:
       array_position = [0,1];
    elif choice == 3:
       array_position = [0,2];
    elif choice == 4:
        array_position = [1,0];
    elif choice == 5:
       array_position = [1,1];
    elif choice == 6:
       array_position = [1,2];
    elif choice == 7:
       array_position = [2,0];
    elif choice == 8:
       array_position = [2,1];
    elif choice == 9:
       array_position = [2,2];
    return array_position