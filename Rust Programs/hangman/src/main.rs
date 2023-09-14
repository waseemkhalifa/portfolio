use std::fs::File;
use std::io::Read;

fn main() {
    let mut vec_data = Vec::new();
    let mut f = File::open("src/words.txt").expect("Unable to open file");
    f.read_to_end(&mut vec_data).expect("Unable to read data");

    println!("");

    let string = String::from_utf8(vec_data).expect("Our bytes should be valid utf8");

    println!("{string}")
}
