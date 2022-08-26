mod settings;
mod game;

fn main() {
    println!("~~~ {} ~~~", settings::TITLE);
    println!("Version {}", settings::VERSION);
    print!("Credit: ");
    for i in 0..settings::CONTRIBUTORS.len() {
        print!("{} ", settings::CONTRIBUTORS[i]);
    }
    println!("");
    let g = game::Game{};
    g.run();
}