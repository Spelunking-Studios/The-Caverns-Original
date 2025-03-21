import pygame

class MenuItem(pygame.sprite.Sprite):
    '''
    A menu object that zooms in and out when hovered over. Requires a position and surface.
    
    Does not currently store whether it has been clicked or not, only serves as a basic object. 
    '''
    def __init__(self, game, pos, image, **kwargs):
        self.game = game
        self.rect = (0, 0, 180, 210)
        self.bgColor = (0, 0, 0, 0)
        #          line (normal)           Rect
        self.hover = False
        self.zoom = 1
        self.zoomMax = 2
        self.zoomMin = 1
        self.zoomSpeed = 0.4
        self.desc = ''
        self.text = ''
        self.groups = []       ## These few lines are the lines for component objects
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(self.rect)
        self.rect.topleft = pos
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        self.imageSrc = pygame.image.load(image)

    def setIcon(self):
        self.icon = pygame.transform.scale(self.imageSrc, (int(self.imageSrc.get_width()*self.zoom), int(self.imageSrc.get_height()*self.zoom)))
        
    def setRect(self):
        self.rect = self.imageSrc.get_rect()
    
    def render(self):
        self.image.fill(self.bgColor)
        self.setIcon()
        rect = self.icon.get_rect(center=(self.rect.w/2, self.rect.h/2))
        self.image.blit(self.icon, rect)
    
    def update(self):
        self.hover = False
        mouseRect = pygame.Rect(self.game.get_mouse_pos()[0], self.game.get_mouse_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        if self.hover:
            self.zoom = min(self.zoomMax, self.zoom + self.zoomSpeed)
        else:
            self.zoom = max(self.zoomMin, self.zoom - self.zoomSpeed)
        
        self.render()
