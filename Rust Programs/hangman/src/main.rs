use std::fs::File;
use std::io::Read;
use std::str;

fn main() {

    let mut string_data = String::new();
    let mut f = File::open("src/words.txt").expect("Unable to open file");
    f.read_to_string(&mut string_data).expect("Unable to read string");
    println!("{:?}", string_data);

    println!("");

    let mut vec_data = Vec::new();
    let mut f = File::open("src/words.txt").expect("Unable to open file");
    f.read_to_end(&mut vec_data).expect("Unable to read data");
    println!("{:?}", vec_data[0]);

    println!("");

    let string = String::from_utf8(vec_data).expect("Our bytes should be valid utf8");

    println!("{string}")
}
