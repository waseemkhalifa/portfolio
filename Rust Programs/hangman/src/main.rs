/* ----------------------- imports ----------------------- */
mod words;
use crate::words::import_words;

/* ----------------------- functions ----------------------- */

fn main() {
    let mut vec_data = Vec::new();
    let vec_data = import_words("src/words.txt");

}
