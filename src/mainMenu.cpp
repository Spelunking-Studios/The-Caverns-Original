#include <vector>
#include "theCaverns.hpp"
#include "ui/menu/component.hpp"
#include "ui/menu/button.hpp"
#include "ui/menu/text.hpp"

void buildMainMenu(void) {
    Menu *mainMenu = new Menu(e);
    e->setMenu(
        e->addMenu(mainMenu)
    );
    TextComponent *title = new TextComponent(mainMenu, "The Caverns", 485, 25);
    ButtonComponent *startBtn = new ButtonComponent(mainMenu, "Start", 485, 500);
    std::vector<MenuComponent*> cs = {
        title,
        startBtn
    };
    for (int i = 0; i < cs.size(); i++) {
        (*mainMenu).addComponent(cs[i]);
    }
}
