use raylib::prelude::*;

use crate::settings;

pub struct Game {}

impl Default for Game {
    fn default() -> Game {
        Game {}
    }
}

impl Game {
    fn init(&self) -> (RaylibHandle, RaylibThread) {
        let (hand, _thread) = raylib::init()
            .size(1200, 700)
            .title(settings::TITLE)
            .build();
        (hand, _thread)
    }
    pub fn run(&self) {
        let (mut rl, _thread) = self.init();
    }
}