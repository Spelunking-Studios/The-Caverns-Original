import pygame

class Image(pygame.sprite.Sprite):
    """Basic Image"""
    def __init__(self, image, game, pos, **kwargs):
        # Load image while attempting to use a predefined image if provided
        if image:
            # Make a copy - not a reference
            print("Using cached image:", image)
            self.trueImage = image.copy()
            self.image = pygame.Surface((64, 64))
        else:
            # No predefined
            self.trueImage = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.trueImage.fill((0, 0, 0, 0))
            self.image = pygame.Surface((64, 64))
        # Colors [normal, hover]
        self.colors = [(50, 50, 50), (60, 60, 0)]
        # Size, Pos
        self.x = pos[0]
        self.y = pos[1]
        self.width = 64
        self.height = 64
        # State
        self.hover = False
        self.clicked = False
        # Event Handlers
        self.onClick = None
        # Other
        self.groups = []
        self.game = game
        # Custom
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        super().__init__(self.groups)

        # Ensure that at least one render is preformed (if update isn't called)
        self.render()
    def drawBG(self, colorIndex = 0):
        """Draw the background color depending on the provided index.
        
        Arguments:
        -----
        colorIndex: int = 0
            And index that is a valid position in self.color. The index must satasfy these bounds:
                - `colorIndex >= 0`
                - `colorIndex < len(self.colors)
        """
        self.image.fill(self.colors[colorIndex])
    def update(self):
        self.hover = False
        self.clicked = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)

        # Check if mouse is hovering over image
        if mouseRect.colliderect(self.rect):
            self.hover = True
            # Check to see if the mouse is also clicking
            for event in self.game.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # We have been clicked on!!!
                    self.clicked = True
                    # Run the click event handler if one exists
                    if self.onClick:
                        self.onClick()
        self.render()
    def render(self):
        # Draw background
        self.drawBG(int(self.hover)) # Typecast from bool to int (True/False) -> (1/0)
        # Draw the image
        self.image.blit(self.trueImage, (0, 0))
    def setClickHandler(self, fn):
        self.onClick = fn