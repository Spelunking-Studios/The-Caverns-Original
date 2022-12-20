from .overlay import Overlay
from menu import Button, Image, Text
from stgs import winWidth, winHeight, fgen
import pygame
from time import time


class InventoryOverlay(Overlay):
    _cached_images = {}

    def __init__(self, game):
        super().__init__(game)
        self.width = winWidth
        self.height = winHeight
        self.image = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        ).convert_alpha()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.last_poll_time = 0
        self.inventory_poll_delay = 100
        self.just_active = False
        self.iitems = []
        self.last_change_time = 0
        self.change_delay = 0.5
        self.item_comps = pygame.sprite.Group()
        self.load_comps()

    def load_comps(self):
        """Loads all of the components"""
        self.menu_bg = pygame.Surface(
            (800, 600),
            pygame.SRCALPHA
        ).convert_alpha()
        self.menu_bg.fill((15, 15, 15, 255))
        self.exit_btn = Button(
            self.game,
            (1020, 60),
            text="X",
            groups=[self.comps],
            center=True,
            rounded=False,
            colors=((20, 20, 20), (50, 50, 50)),
            textColors=((100, 100, 100), (100, 100, 100)),
            wh=(20, 20)
        )
        self.items_btn = Button(
            self.game,
            (240, 60),
            center=True,
            text="Items",
            groups=[self.comps],
            colors=((20, 20, 20), (50, 50, 50)),
            textColors=((100, 100, 100), (100, 100, 100)),
            wh=(80, 20),
            rounded=False
        )

    def poll_inventory(self):
        """Poll the inventory for items"""
        # Fetch the items in the inventory
        self.iitems = self.game.player.inventory.get_items()

        # Destroy all of the components
        for item in self.item_comps:
            item.kill()

        # Identify the player's equipped weapon
        player_equipped_weapon = self.game.player.equippedWeapon.__class__.__name__

        # Setup the loop
        ix = 0
        iy = 0
        for item in self.iitems:
            if item not in self._cached_images:
                print(
                    "\x1b[36mInventoryOverlay:",
                    f"caching renderable for {item} item\x1b[0m"
                )
                if (
                    len(self.iitems[item]["items"]) and
                    self.iitems[item]["items"][0].renderable
                ):
                    self._cached_images[item] = pygame.transform.scale(
                        self.iitems[item]["items"][0].renderable,
                        (64, 64)
                    )
                else:
                    print(
                        "\x1b[93mInventoryOverlay: Warning:",
                        "no renderable found for the item,",
                        "using a placeholder.\x1b[0m"
                    )
                    self._cached_images[item] = pygame.Surface(
                        (64, 64),
                        pygame.SRCALPHA
                    ).convert_alpha()
            imref = self._cached_images[item]
 
            # Create the image component
            pos = (
                (self.width / 2 - 400) + 10 + (80 * ix),
                (self.height / 2 - 300) + 30 + (90 * iy)
            )
            i = Image(imref, self.game, pos, groups=[self.item_comps], iitem=item)
            i.setClickHandler(self.handle_item_click)

            # Create a label if the item is also the player's current wepon
            if item == player_equipped_weapon:
                print("Player has", item, "equipped.")
                font = fgen("ComicSansMS.ttf", 12)
                text = Text(font, "Equipped", (255, 255, 255), pos=(pos[0] + 6, pos[1] + 66), groups=[self.item_comps])

            # Update positioning variables
            ix += 1
            if ix > 2:
                ix = 0
                iy += 1

    def handle_item_click(self, caller):
        # Load info about the item
        item_name = caller.iitem
        entry = self.game.player.inventory._registry["items"].get(item_name, None)
        
        if entry:
            # Make sure the item isn't already equipped
            if self.game.player.equippedWeapon.__class__.__name__ == item_name:
                print("The player already has '" + item_name + "' equipped.")
                return

            # Set the player's equipped weapon
            self.game.player.equippedWeapon = entry["items"][0]
            
            # Print a message to the console
            print("Changed the player's equipped weapon to '" + item_name + "'.")

            # Force a rerender of the overlay
            self.poll_inventory()
            self.render()
        else:
            print(
                "\x1b[93Warning:",
                "Could not find an inventory entry for the '" + item_name + "'",
                "item.\x1b[0m"
            )

    def update(self):
        """Update (DUH)"""
        if self.active:
            if self.exit_btn.clicked:
                self.deactivate()
            if (
                time() - self.last_poll_time >= self.inventory_poll_delay or
                self.just_active
            ):
                self.poll_inventory()
                self.last_poll_time = time()
            self.comps.update()
            self.item_comps.update()
            self.render()
            self.just_active = False

    def can_activate(self):
        """A simple functaion that returns a boolean \
        based on if the overlay can activate"""
        return time() - self.last_change_time >= self.change_delay

    def activate(self):
        if self.can_activate():
            self.last_change_time = time()
            super().activate()
            if not self.game.inInventory:
                print(
                    "\x1b[93mWarning:",
                    "game's inventory overlay was not open.",
                    "Opening it...\x1b[0m"
                )
                self.game.openInventory()
            self.just_active = True

    def deactivate(self):
        """Deactivate the inventory"""
        super().deactivate()
        self.last_change_time = time()
        if self.game.inInventory:
            print(
                "\x1b[93mWarning:",
                "game's inventory overlay was not closed.",
                "Closing it...\x1b[0m"
            )
            self.game.closeInventory()

    def render(self):
        """Render the inventory"""
        self.image.fill((0, 0, 0, 127))
        self.image.blit(self.menu_bg, self.get_offset())
        for comp in self.comps:
            self.image.blit(comp.image, comp.rect)
        for item_comp in self.item_comps:
            self.image.blit(item_comp.image, item_comp.rect)

    def get_offset(self):
        """Get the position of the upper left corner of the overlay

        Returns: tuple (x, y)
        """
        return (self.width / 2 - 400, self.height / 2 - 300)
