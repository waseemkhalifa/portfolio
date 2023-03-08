/* ----------------- Text based rock paper scissors game ------------- */
/*
    This is a simple text based rock paper scissors game coded in Rust

    The concept of the game is very simple:
    > the player will be asked to choose one of rock paper scissors
    > the computer will choose rock paper scissors at random
    > depending on who wins the round, will get one point
    > at the end of each round the player will be asked if they want to
    continue playing or not

    The rules of rock paper scissors is as follows:
    rock beats scissors, scissors beats paper, paper beats rock
*/

/* ----------------------- main ----------------------- */
fn main() {
    
    // our HashMap will store rock, paper & scissors as key value pairs
    let mut hm_choice: HashMap<i32, String> = HashMap::new();
    hm_choice.insert(1, "Rock".to_string());
    hm_choice.insert(2, "Paper".to_string());
    hm_choice.insert(3, "Scissors".to_string());

    // these are our score variables for the players
    let mut player_score:i32 = 0;
    let mut computer_score:i32 = 0;

    // this is our main game
    let mut play:bool = true;
    while play == true {

        // we'll ask the player for their choice
        let player = players_choice();
        // get the string value from hashmap
        let player = hm_choice.get(&player).unwrap();

        //  the computer's random choice
        let computer = computer_choice();
        // get the string value from hashmap
        let computer = hm_choice.get(&computer).unwrap();

        // we'll print the choices
        println!("");
        println!("Player:{}     Computer:{}", player, computer);

        // we'll print out the result of the round
        let result = won_lost(player, computer);
        println!("");
        println!("{}", result);

        // we'll work out the scores
        player_score = player_new_score(player_score, result);
        computer_score = computer_new_score(computer_score, result);
        println!("");
        println!("SCORE:    Player={}     Computer={}", 
            player_score, computer_score);
        
        // we'll ask the player if they want to continue playing the game
        play = continue_playing();
    }

}

/* ----------------------- packages ----------------------- */
// this will be used by the computer to choose rock paper scissors at random
use rand::Rng;
// this will store our rock, paper & scissors as key value pairs
use std::collections::HashMap;
// this will allow the user to input their choice for the game
use std::io;

/* ----------------------- functions ----------------------- */
// this function will ask the player for their choice
// it will return only the valid input of 1, 2 or 3, which we'll map
// to our hashmap
fn players_choice() -> i32 {

    // the only values we'll accept for our user input
    let correct_input: [i32; 3] = [1, 2, 3];

    // this is a loop, which will only end if a valid input is entered
    let choice = loop {
        println!("");
        println!("Choose one of the following:");
        println!("Rock(1), Paper(2) or Scissors(3)");

        // this is Rust's user input method
		let mut choice = String::new();
		io::stdin().read_line(&mut choice).unwrap();

        // if the value entered was int
		if let Ok(val) = choice.trim().parse::<i32>() {
            if correct_input.contains(&val) {
                break val;
            }
            // this will bring if the value wasn't our valid input values
            println!("");
            println!("Wrong Input!");
            println!("Only 1, 2 or 3 are valid inputs");
            println!("");
			continue;
		}

        // this will be printed if the value entered was not int
        println!("");
        println!("Wrong Input!");
        println!("Only 1, 2 or 3 are valid inputs");
        println!("");
	};

    return choice;
}

// this function will return the computer's choice (at random)
fn computer_choice() -> i32 {
    // this retuns a  random value between 1 and 3
    let choice: i32 = rand::thread_rng().gen_range(1..4);
    return choice;
}

// this function will work who has won or lost the round
fn won_lost<'a>(player_chosen: &'a str, computer_chosen: &'a str) -> &'a str {

    let mut return_value: &str = "";

    // if player and computer have the same choice
    if player_chosen == computer_chosen {
        return_value = "DRAW!";
    // player wins
    } else if player_chosen == "Rock" && computer_chosen == "Scissors" {
        return_value = "YOU WIN!";
    } else if player_chosen == "Paper" && computer_chosen == "Rock" {
        return_value = "YOU WIN!";
    } else if player_chosen == "Scissors" && computer_chosen == "Paper" {
        return_value = "YOU WIN!";
    // computer wins
    } else if computer_chosen == "Rock" && player_chosen == "Scissors" {
        return_value = "YOU LOSE!";
    } else if computer_chosen == "Paper" && player_chosen == "Rock" {
        return_value = "YOU LOSE!";
    } else if computer_chosen == "Scissors" && player_chosen == "Paper" {
        return_value = "YOU LOSE!";
    }

    return return_value;
}

// this function will work out the player's score
fn player_new_score(score:i32, result:&str) -> i32 {
    let mut new_score = score;
    if result == "YOU WIN!" {
        new_score += 1;
    }

    return new_score;
}

// this function will work out the computer's score
fn computer_new_score(score:i32, result:&str) -> i32 {
    let mut new_score = score;
    if result == "YOU LOSE!" {
        new_score += 1;
    }

    return new_score;
}

// this function will ask the player if they'd like to continue playing
fn continue_playing() -> bool {
    // the only values we'll accept for our user input
    let correct_input: [i32; 2] = [1, 2];

    // this is a loop, which will only end if a valid input is entered
    let choice = loop {
        println!("");
        println!("Continue playing?: Yes(1) or No(2):");

        // this is Rust's user input method
		let mut choice = String::new();
		io::stdin().read_line(&mut choice).unwrap();

        // if the value entered was int
		if let Ok(val) = choice.trim().parse::<i32>() {
            if correct_input.contains(&val) {
                break val;
            }
            // this will bring if the value wasn't our valid input values
            println!("");
            println!("Wrong Input!");
            println!("Only 1 or 2 are valid inputs");
            println!("");
			continue;
		}

        // this will be printed if the value entered was not int
        println!("");
        println!("Wrong Input!");
        println!("Only 1 or 2 are valid inputs");
        println!("");
	};

    // convert the input to True or False
    if choice == 1 {
        println!("");
        return true;
    } else {
        println!("");
        println!("Thank you for playing - GOODBYE");
        return false;
    }
}

