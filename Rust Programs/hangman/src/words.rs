/*
    this file will look after import of words for the hangman
    we'll import words into a vector of bytes 
    we'll have a function to convert the bytes to string format
*/ 


/* ----------------------- imports ----------------------- */
use std::fs::File;
use std::io::Read;

/* ----------------------- functions ----------------------- */

fn import_words(file_name:string) {
    let mut vec_data = Vec::new();
    let mut f = File::open(file_path).expect("Unable to open file");
    f.read_to_end(&mut vec_data).expect("Unable to read data");
}




