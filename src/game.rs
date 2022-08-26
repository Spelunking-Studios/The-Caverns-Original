use raylib::prelude::*;

pub struct Game;

impl Defautl for Game {
    fn default() -> Game {
        Game {}
    }
}

impl Game {
    fn init(&self) {
        
    }
    pub fn run(&self) {
        self.init();
    }
}