#include <vector>
#include "theCaverns.hpp"

void buildMainMenu(void) {
    Menu *mainMenu = new Menu(e);
    e->setMenu(
        e->addMenu(mainMenu)
    );
    std::vector<MenuComponent*> cs = {
        new TextComponent(mainMenu, "The Caverns", 485, 25)
    };
    for (int i = 0; i < cs.size(); i++) {
        (*mainMenu).addComponent(cs[i]);
    }
}