from .overlay import Overlay
from menu import Button, Image, Text
from stgs import winWidth, winHeight, fgen
import src.util.colors as colors
import menu
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
        self.load_comps()
        self.tooltip_last = None
        self.tooltip_ac = 0
        self.tooltip_id = None

        # Random settings
        self.maxToolTipSize = 300
        self.padding = 8

    def load_comps(self):
        """Loads all of the components"""
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
                        (64, 64)
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
                        (64, 64),
                        pygame.SRCALPHA
                    ).convert_alpha()

            # Grab the image out of cache
            imref = self._cached_images[item_id]

            # Create the image component
            pos = (
                (self.width / 2 - 400) + 10 + (80 * ix),
                (self.height / 2 - 300) + 30 + (90 * iy)
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

            # Create a label if the item is also the player's current wepon
            if item_id == player_equipped_weapon:
                print("Player has", item_id, "equipped.")
                font = fgen("ComicSansMS.ttf", 12)
                Text(
                    font,
                    "Equipped",
                    (255, 255, 255),
                    pos=(pos[0] + 6, pos[1] + 66),
                    groups=[self.item_comps]
                )

            # Update positioning variables
            if ix + 1 > 2:
                ix = 0
                iy += 1
            else:
                ix += 1

        # Regenerate the base image with the new items
        self.render_base()

    def handle_item_click(self, caller):
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

        # Draw tooltip

        # If no time exists, set it
        if not self.tooltip_last:
            self.tooltip_last = time()

        # Set some base variables
        mpos = self.game.get_mouse_pos()  # Mouse position
        found = False  # If the comp that is hovered over is found

        # Search through all of the item components till we find
        # the one that is being hovered over
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
                        self.render_tooltip(item_comp)

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
        pygame.draw.rect(self.base_image, (15, 15, 15), (*self.get_offset(), 800, 600))

        # Draw non-item comps
        for comp in self.comps:
            self.base_image.blit(comp.image, comp.rect)

        # Draw items
        for item_comp in self.item_comps:
            self.base_image.blit(item_comp.image, item_comp.rect)

    def render_tooltip(self, item_comp):
        """Render the tooltip for a given item component"""
        # Generate all of the fonts that are going to be used
        title_font = fgen("PixelLove.ttf", 18)

        # Render the text
        tooltip_title = title_font.render(
            item_comp.tooltip[0],
            True,
            (255, 255, 255)
        )
        tooltip_desc = menu.Text(
            fgen("ComicSansMS.ttf", 12),
            item_comp.tooltip[1],
            colors.white,
            True,
            multiline=True,
            size=(self.maxToolTipSize - self.padding * 2, 900)
        )

        # Determine the size of the box we need
        width = self.maxToolTipSize
        height = tooltip_title.get_height() + tooltip_desc.last_rendered_y \
            + self.padding * 3  # 3 to account for padding between title and desc

        # Common values
        title_y = item_comp.rect.y + self.padding
        desc_y = title_y + tooltip_title.get_height() + self.padding
        tooltip_x_start = item_comp.rect.x + item_comp.rect.width + 5

        # Draw the box
        pygame.draw.rect(
            self.image,
            (40, 40, 40),
            (
                tooltip_x_start,
                item_comp.rect.y,
                width,
                height
            )
        )

        # Draw on the title
        self.image.blit(tooltip_title, (tooltip_x_start + self.padding, title_y))

        # Draw on the description
        self.image.blit(tooltip_desc.image, (tooltip_x_start + self.padding, desc_y))

    def get_offset(self):
        """Get the position of the upper left corner of the overlay

        Returns: tuple (x, y)
        """
        return (self.width / 2 - 400, self.height / 2 - 300)
