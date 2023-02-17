/*
    Text based rock paper scissors game

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

// this will be used by the computer to choose rock paper scissors at random
use rand::Rng;

fn main() {
    
    let mut rng = rand::thread_rng();
    println!("Random Value: {}", rng.gen_range(1..4));

}

