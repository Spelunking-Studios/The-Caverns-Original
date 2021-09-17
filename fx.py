from stgs import *
from animations import animation
import colors
import random

#### All screen effects/fx will be done in the fx specific layer or in the overlay.
#  Duration should be handled by the fx object.
#  Fx initiation into the fx layer will record its instance
#  
class fadeOut(pygame.sprite.Sprite):
    alpha = 0
    speed = 4 
    fadeBack = False
    def __init__(self, game, **kwargs):
        self.game = game
        self.onEnd = False
        self.noKill = False
        self.ended = False
        self.color = (0, 0, 0)
        self.startDelay = 0
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.onEnd:
            self.groups = game.pSprites, game.fxLayer
        else:
            self.groups = game.sprites, game.fxLayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.intTime = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.intTime >= self.startDelay:
            if self.alpha > 220:
                if self.fadeBack:
                    fadeIn(self.game)
                self.end()
                self.ended = True
            else:
                self.alpha += self.speed

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd and not self.ended:
            self.onEnd()
        if not self.noKill:
            self.kill()

class fadeIn(pygame.sprite.Sprite):
    alpha = 255
    speed = 5 

    def __init__(self, game, **kwargs):
        self.game = game
        self.onEnd = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.onEnd:
            self.groups = game.pSprites, game.fxLayer
        else:
            self.groups = game.sprites, game.fxLayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))

    def update(self):
        if self.alpha < 2*self.speed:
            self.end()
        else:
            self.alpha -= self.speed

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd:
            self.onEnd()
        self.kill()

#class timer(pygame.sprite):
#    def __init__(self, game, duration=600):

class particles(pygame.sprite.Sprite):
    def __init__(self, game, entity, **kwargs):
        self.game = game
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = 12
        self.tickSpeed = 40
        self.lifeSpan = False
        self.hide = False
        self.particleKwargs = {}
        self.dirRange = (0, 360)
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.lastParticle = 0
        try:
            self.entityRect = entity.rect
        except:
            self.entityRect = entity
        self.init = pygame.time.get_ticks()
        self.particles = pygame.sprite.Group()

    def update(self):
        if not self.hide:
            self.addParticles()
        self.particles.update()
        if self.lifeSpan:
            if pygame.time.get_ticks() - self.init >= self.lifeSpan:
                self.end()

    def addParticles(self):
        if len(self.particles) < self.size and pygame.time.get_ticks() - self.lastParticle >= self.tickSpeed:
            self.particles.add(particle(self.game, pygame.Vector2(1, 0).rotate(random.randint(self.dirRange[0], self.dirRange[1])), pygame.Vector2(self.entityRect.center), self.particleKwargs))
            self.lastParticle = pygame.time.get_ticks()

    def setParticleKwargs(self, **kwargs):
        self.particleKwargs = {}
        for k, v in kwargs.items():
            self.particleKwargs[k] = v

    def end(self):  
        self.kill()
    
    def kill(self):
        for p in self.particles:
            p.kill()
        super().kill()

class playerParticles(particles):
    def __init__(self, game, entity):
        self.entity = entity
        super().__init__(game, entity, size = 6, dirRange=(140, 220), tickSpeed=80)
        self.setParticleKwargs(color=colors.rgba(colors.grey, 120), speed=-0.2, size=(15,15), shrink=0.5, life=200)
        self.step = 90

    def update(self):
        self.entityRect = self.entity.rect
        super().update()
  
    def addParticles(self):
        if len(self.particles) < self.size and pygame.time.get_ticks() - self.lastParticle >= self.tickSpeed:
            try:
                dir = self.entity.vel.normalize()
                pos = pygame.Vector2(self.entityRect.center)
                pos += dir.rotate(self.step) * 10
                self.step*=-1
                dir.rotate_ip(random.randint(self.dirRange[0], self.dirRange[1]))
                self.particles.add(particle(self.game, dir, pos, self.particleKwargs))
                self.lastParticle = pygame.time.get_ticks()
            except:
              pass
 

class particle(pygame.sprite.Sprite):
    def __init__(self, game, dir, pos, kwargs):
        self.game = game
        self.groups = game.layer1
        #self.alpha = 255
        self.speed = 2.5
        self.shrink = 0.2
        self.life = 600
        self.color = colors.red
        self.size = (10, 10)
        self.dir = dir
        self.pos = pos
        pygame.sprite.Sprite.__init__(self, self.groups)
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.init = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.w = self.size[0]
        self.rect.center = self.pos.x, self.pos.y
        self.render()

    def render(self):
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.rect.width/2, self.rect.height/2), self.w/2)

    def update(self):
        self.pos += self.dir*self.speed
        self.rect.center = self.pos.x, self.pos.y
        self.w -= self.shrink
        self.render()
        if pygame.time.get_ticks() - self.init >= self.life:
            self.kill()
        


### This is pretty pointless but eyy
class highlight(pygame.sprite.Sprite):
    def __init__(self, game, entity, **kwargs):
        self.game = game
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        for k, v in kwargs.items():
            self.__dict__[k] = v
        self.entity = entity
        self.entImgRect = pygame.Rect(entity.rect.x, entity.rect.y, self.entity.image.get_width(), self.entity.image.get_height())
        self.rect = pygame.Rect(self.entImgRect)
        self.render()

    def render(self):
        self.rect.w = self.entImgRect.w*1.2
        self.rect.h = self.entImgRect.h*1.2
        self.image = pygame.transform.scale(self.entity.image, (self.rect.w, self.rect.h))
        self.image.fill((255, 255, 255), special_flags = pygame.BLEND_MAX)
    
    def update(self):
        self.entImgRect = pygame.Rect(self.entity.rect.x, self.entity.rect.y, self.entity.image.get_width(), self.entity.image.get_height())
        self.render()
        self.rect.center = self.entImgRect.center
