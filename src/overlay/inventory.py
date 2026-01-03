from .overlay import Overlay
from .components import Tooltip
from src.menu import Button, Image, Text
from src import stgs
from src.stgs import fonts
import src.util.colors as colors
import pygame
from time import time


class InventoryOverlay(Overlay):
    _cached_images = {}

    # Tabs
    ITEMS_TAB= 0
    STATS_TAB = 1

    # UI
    SLOT_WIDTH = 80
    SLOT_HEIGHT = 90
    SLOT_IMG_WIDTH = 64
    SLOT_IMG_HEIGHT = 64
    SLOT_OFFSET_X = 10
    SLOT_OFFSET_Y = 30
    SLOT_LABEL_PADDING = 2
    SLOT_WRAP_LIMIT = 5
    EQUIPMENT_ZONE_WIDTH = SLOT_WIDTH * 3
    EQUIPMENT_LABELS = ["Neck", "Bracers", "Boots"]

    def __init__(self, game):
        super().__init__(game)
        self.width = self.game.width()
        self.height = self.game.height()
        self.panel_width = 800
        self.image = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        ).convert_alpha()
        self.base_image = pygame.Surface(
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
        self.equipment_comps = pygame.sprite.Group()
        self.equipment_comp_bases = []
        self.stats_comps = pygame.sprite.Group()

        self.tooltip_last = None
        self.tooltip_ac = 0
        self.tooltip_id = None

        self.tabs = ["items_btn", "stats_btn"]
        self.current_tab = self.ITEMS_TAB

        self.load_comps()

        # Random settings
        self.maxToolTipSize = 300
        self.padding = 8

    def load_comps(self):
        """Loads all of the components"""
        self.exit_btn = Button(
            self.game,
            (self.get_offset()[0]+self.panel_width-20, self.get_offset()[1]-20),
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
            (self.get_offset()[0], self.get_offset()[1]-20),
            center=True,
            text="Items",
            groups=[self.comps],
            colors=[(20, 20, 20), (50, 50, 50)],
            textColors=((100, 100, 100), (100, 100, 100)),
            wh=(80, 20),
            rounded=False,
            activeTabColor=(30, 30, 30),
            inactiveTabColor=(20, 20, 20),
            onClickContext=self.tabBtnClickHandler
        )
        self.stats_btn = Button(
            self.game,
            (self.get_offset()[0]+80, self.get_offset()[1]-20),
            center=True,
            text="Stats",
            groups=[self.comps],
            colors=[(20, 20, 20), (50, 50, 50)],
            textColors=((100, 100, 100), (100, 100, 100)),
            wh=(80, 20),
            rounded=False,
            activeTabColor=(30, 30, 30),
            inactiveTabColor=(20, 20, 20),
            onClickContext=self.tabBtnClickHandler
        )

        # Base images for the equipment slots
        self.equipment_comp_bases = [
            pygame.Surface((64, 64), pygame.SRCALPHA),
            pygame.Surface((64, 64), pygame.SRCALPHA),
            pygame.Surface((64, 64), pygame.SRCALPHA)
        ]
        self.regenerate_equipment_comps()

        # Load stats components
        Text(
            "3",
            "Statistics",
            colors.white,
            stgs.aalias,
            pos=(100, 100),
            groups=[self.stats_comps]
        )
        Text(
            "menu2",
            "Health: -1",
            colors.white,
            stgs.aalias,
            pos=(100, 150),
            groups=[self.stats_comps],
            update_hook=lambda: f"Health: {self.game.player.stats.health}"
        )
        Text(
            "menu2",
            "Strength: -1",
            colors.white,
            stgs.aalias,
            pos=(100, 175),
            groups=[self.stats_comps],
            update_hook=lambda: f"Strength: {self.game.player.stats.strength}"
        )
        Text(
            "menu2",
            "Speed: -1",
            colors.white,
            stgs.aalias,
            pos=(100, 200),
            groups=[self.stats_comps],
            update_hook=lambda: f"Speed: {self.game.player.stats.speed}"
        )
        Text(
            "menu2",
            "Armor: Placeholder",
            colors.white,
            stgs.aalias,
            pos=(100, 225),
            groups=[self.stats_comps],
        )
        Text(
            "menu2",
            "Critical Hit Chance: +0% (Placeholder)",
            colors.white,
            stgs.aalias,
            pos=(100, 250),
            groups=[self.stats_comps],
            # update_hook=lambda: f"Critical Hit Chance: {self.game.player.stats.crit}%"
        )

        self.set_current_tab(0)

    def set_current_tab(self, tab_index):
        # Deactive the current tab button
        btn = getattr(self, self.tabs[self.current_tab], None)
        if btn:
            btn.colors[0] = btn.inactiveTabColor

        # Activate the new current tab button
        self.current_tab = tab_index
        btn = getattr(self, self.tabs[self.current_tab], None)
        if btn:
            btn.colors[0] = btn.activeTabColor

    def tabBtnClickHandler(self, btn):
        tab_index = self.tabs.index(btn.text.lower() + "_btn")
        self.set_current_tab(tab_index)

    def regenerate_equipment_comps(self):
        slot_left = (self.width / 2 - 400) + self.SLOT_OFFSET_X + self.SLOT_WIDTH
        for i, base in enumerate(self.equipment_comp_bases):
            pos = (
                slot_left,
                (self.height / 2 - 300) + self.SLOT_OFFSET_Y + (self.SLOT_HEIGHT * i)
            )
            Image(
                base,
                self.game,
                pos,
                groups=[self.equipment_comps]
            )
            label = Text(
                fonts["label+"],
                self.EQUIPMENT_LABELS[i],
                colors.white,
                stgs.aalias,
                (pos[0], pos[1] + self.SLOT_LABEL_PADDING + self.SLOT_IMG_WIDTH),
                groups=[self.equipment_comps]
            )

            # We have to do some shenanigans to center the label text
            label.pos.x = pos[0] + (self.SLOT_IMG_WIDTH / 2) - (label.image.get_width() / 2)
            label.setText(self.EQUIPMENT_LABELS[i])

    def poll_inventory(self):
        """Poll the inventory for items"""
        # Make a variable for convenience
        inventory = self.game.player.inventory

        # Fetch the items in the inventory
        self.iitems = inventory.get_items()

        # Destroy all of the components
        for item in self.item_comps:
            item.kill()

        # Identify the player's equipped weapon
        player_equipped_weapon = getattr(self.game.player.slot1, "id", None)

        # Setup the loop
        ix = 0
        iy = 0

        # Loop over each item
        for item_id in self.iitems:
            # Retrive the item from the inventory
            item = inventory.get_item(item_id)

            # Make sure the image exists in the cache
            if item_id not in self._cached_images:
                # Print an info message
                print(
                    "\x1b[36mInventoryOverlay:",
                    f"caching renderable for {item_id} item\x1b[0m"
                )

                # If the item has an image, cache it
                # Otherwise, create a dummy image
                if item.renderable:
                    self._cached_images[item_id] = pygame.transform.scale(
                        item.renderable,
                        (self.SLOT_IMG_WIDTH, self.SLOT_IMG_HEIGHT)
                    )
                else:
                    # Print a warning message for devs
                    print(
                        "\x1b[93mInventoryOverlay: Warning:",
                        "no renderable found for the item,",
                        "using a placeholder.\x1b[0m"
                    )

                    # Add a placeholder into the cache
                    self._cached_images[item_id] = pygame.Surface(
                        (self.SLOT_IMG_WIDTH, self.SLOT_IMG_HEIGHT),
                        pygame.SRCALPHA
                    ).convert_alpha()

            # Grab the image out of cache
            imref = self._cached_images[item_id]

            # Create the image component
            x_offsets = self.EQUIPMENT_ZONE_WIDTH + self.SLOT_OFFSET_X
            pos = (
                (self.width / 2 - 400) + x_offsets + (self.SLOT_WIDTH * ix),
                (self.height / 2 - 300) + self.SLOT_OFFSET_Y + (self.SLOT_HEIGHT * iy)
            )
            i = Image(
                imref,
                self.game,
                pos,
                groups=[self.item_comps],
                iitem=item_id,  # Custom! Not used by the actual image at all
                tooltip=(
                    item.kind,
                    item.stats["description"]
                ),  # Also custom
                ukey=item_id  # Custom key to uid the element
            )
            i.setClickHandler(self.handle_item_click)

            # Create a label if the item is also the player's current weapon
            if item_id == player_equipped_weapon:
                print("Player has", item_id, "equipped.")
                label = Text(
                    fonts["label"],
                    "Equipped",
                    (255, 255, 255),
                    pos=(pos[0], pos[1] + self.SLOT_LABEL_PADDING + self.SLOT_IMG_HEIGHT),
                    groups=[self.item_comps]
                )
                label.pos.x = pos[0] + (self.SLOT_IMG_WIDTH / 2) - (label.image.get_width() / 2)
                label.setText("Equipped")

            if "wearable" in item.get_categories() and item.stats["equipped"]:
                if "necklace" in item.get_categories():
                    self.equipment_comp_bases[0] = item.renderable
                elif "gloves" in item.get_categories():
                    self.equipment_comp_bases[1] = item.renderable
                elif "boots" in item.get_categories():
                    self.equipment_comp_bases[2] = item.renderable

            # Update positioning variables
            if ix + 1 > self.SLOT_WRAP_LIMIT:
                ix = 0
                iy += 1
            else:
                ix += 1

        # Regenerate the base image with the new items
        self.render_base()
        self.regenerate_equipment_comps()

    def handle_item_click(self, caller, type=0):
        # Load info about the item
        item_id = caller.iitem
        entry = self.game.player.inventory._registry["items"].get(
            item_id,
            None
        )

        if entry:
            # Make sure the item isn't already equipped
            if getattr(self.game.player.slot1, "id", None) == item_id:
                print("The player already has '" + item_id + "' equipped.")
                return

            if "weapon" in entry.get_categories():

                # Set the player's equipped weapon
                self.game.player.slot1 = entry

                # Print a message to the console
                print(
                    "Changed the player's equipped weapon to",
                    "'" + item_id + "'."
                )

                # Force a rerender of the overlay
                self.poll_inventory()
                self.render()
            elif "wearable" in entry.get_categories():
                entry.equip(self.game)
                # Add to necklace slot
                if "necklace" in entry.get_categories():
                    self.equipment_comp_bases[0] = entry.renderable

                self.regenerate_equipment_comps()

            elif "note" in entry.get_categories():
                self.game.dialogueScreen.dialogueFromText(entry.get_text())

        else:
            print(
                "\x1b[93Warning:",
                "Could not find an inventory entry for the",
                "'" + item_id + "'",
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
            self.equipment_comps.update()
            self.stats_comps.update()

            # Stats components are special because they can track variables
            if self.current_tab == self.STATS_TAB:
                for comp in self.stats_comps:
                    if getattr(comp, "update_hook", None):
                        comp.setText(comp.update_hook())

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
            self.render_base()

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
        self.render_base()
        self.image.blit(self.base_image, (0, 0))

        # If no time exists, set it
        if not self.tooltip_last:
            self.tooltip_last = time()

        # Set some base variables
        mpos = self.game.get_mouse_pos()  # Mouse position
        found = False  # If the comp that is hovered over is found

        # Search through all of the item components till we find
        # the one that is being hovered over
        if self.current_tab == self.ITEMS_TAB:
            for item_comp in self.item_comps:
                if not isinstance(item_comp, Image):
                    continue

                # Check to see if the mouse is over the component
                over = item_comp.rect.collidepoint(mpos)

                if over:
                    # Check to see if we are still hovering over the same image
                    if self.tooltip_id == item_comp.ukey or not self.tooltip_id:
                        # Add to accumulator and update the last time
                        self.tooltip_ac += time() - self.tooltip_last
                        self.tooltip_last = time()

                        # Mark the found flag (since we did find it)
                        found = True

                        # If the mouse has been over the component long enough
                        # show the tooltip
                        if self.tooltip_ac >= 0.25:
                            tooltip = Tooltip(*item_comp.tooltip, self.padding)

                            tooltip_x_start = item_comp.rect.x + item_comp.rect.width + 5
                            tooltip_y_start = item_comp.rect.y

                            tooltip.render(self.image, tooltip_x_start, tooltip_y_start)

                    # Update the tooltip key to match the now hovered image
                    self.tooltip_id = item_comp.ukey

                    # We found what we are looking for so why continue
                    break

        # If nothing could be found, clear the accumulator
        if not found:
            self.tooltip_ac = 0

    def render_base(self):
        """Render the base surface of the inventory (no tooltips)"""
        # Draw BG
        self.base_image.fill((0, 0, 0, 127))
        pygame.draw.rect(self.base_image, (15, 15, 15), (*self.get_offset(), self.panel_width, 600))

        # Draw non-item comps
        for comp in self.comps:
            self.base_image.blit(comp.image, comp.rect)

        if self.current_tab == self.ITEMS_TAB:
            for item_comp in self.item_comps:
                self.base_image.blit(item_comp.image, item_comp.rect)
            for eq_slot in self.equipment_comps:
                self.base_image.blit(eq_slot.image, eq_slot.rect)
        elif self.current_tab == self.STATS_TAB:
            for component in self.stats_comps:
                self.base_image.blit(component.image, component.rect.move(self.get_offset()))

    def get_offset(self):
        """Get the position of the upper left corner of the overlay

        Returns: tuple (x, y)
        """
        return (self.width / 2 - 400, self.height / 2 - 300)
