/* ----------------------- packages ----------------------- */
// this will allow us to iterate over a Enum
use strum::IntoEnumIterator;
use strum_macros::EnumIter;

/* ----------------------- functions ----------------------- */
pub struct Player {
    bank: 100,
    hand: Vec<Card>,
    bet: 0,
    hand_value: 0
}