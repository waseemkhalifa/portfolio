/*
    this file will look after import of words for the hangman
    we'll import words into a vector of bytes 
    we'll have a function to convert the bytes to string format
*/ 

/* ----------------------- imports ----------------------- */
use std::fs::File;
use std::io::Read;

/* ----------------------- functions ----------------------- */

pub fn import_words(file_path:&str) {

    let mut vec_data: Vec<u8> = Vec::new();
    let mut f = File::open(file_path).expect("Unable to open file");
    f.read_to_end(&mut vec_data).expect("Unable to read data");

}

// pub fn bytes_to_string(word:&str, vec_data:Vec) -> &str {

//     let word_stringed = String::from_utf8(vec_data).
//         expect("Our bytes should be valid utf8");

//     return word_stringed;
// }
