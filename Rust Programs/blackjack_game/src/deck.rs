// the derive attribute makes the enum printable
#[derive(Debug, EnumIter, Copy, Clone)]
enum Suits {
    Hearts, 
    Diamonds, 
    Spades, 
    Clubs
}

// the derive attribute makes the enum printable
#[derive(Debug, EnumIter, Copy, Clone)]
enum Ranks {
    Two, 
    Three, 
    Four, 
    Five, 
    Six, 
    Seven, 
    Eight, 
    Nine, 
    Ten, 
    Jack, 
    Queen, 
    King, 
    Ace
}
#[derive(Debug, Copy, Clone)]
struct Card {
    suit:Suits,
    rank:Ranks
}

pub fn create_deck() -> Vec<Card> {
    let mut deck:Vec<Card>  = vec![];
    for suits in Suits::iter() {
        for ranks in Ranks::iter() {
            let a = suits;
            let b = ranks;
            let card = Card{suit:a, rank:b};
            deck.push(card);
        }
    }
    return deck;
}