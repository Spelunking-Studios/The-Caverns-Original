from src import util
from src.stgs import *
#from animations import animation
import src.util.colors as colors
import random

#### All screen effects/fx will be done in the fx specific layer or in the overlay.
#  Duration should be handled by the fx object.
#  Fx initiation into the fx layer will record its instance
#  
class FadeOut(util.Sprite):
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

        self.rect = pygame.Rect(0, 0, self.game.width(), self.game.height())
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        self.intTime = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.intTime >= self.startDelay:
            if self.alpha > 220:
                if self.fadeBack:
                    FadeIn(self.game)
                self.end()
                self.ended = True
            else:
                self.alpha += self.speed * self.game.dt2()

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd and not self.ended:
            print("why isnt the buttons showing")
            self.onEnd()
        if not self.noKill:
            self.kill()

class FadeIn(util.Sprite):
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

        self.rect = pygame.Rect(0, 0, self.game.width(), self.game.height())
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height)).convert_alpha()

    def update(self):
        if self.alpha < 2*self.speed:
            self.end()
        else:
            self.alpha -= self.speed* self.game.dt2()

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd:
            self.onEnd()
        self.kill()

#class timer(util):
#    def __init__(self, game, duration=600):

class Particles(util.Sprite):
    def __init__(self, game, entity, **kwargs):
        self.game = game
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = 12
        self.tickSpeed = 40
        self.lifeSpan = False
        self.hide = False
        self.particleKwargs = {}
        self.particleType = Particle
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
    
    def setLife(self, time):
        self.lifeSpan = time
        self.init = pygame.time.get_ticks()

    def addParticles(self):
        if len(self.particles) < self.size and pygame.time.get_ticks() - self.lastParticle >= self.tickSpeed:
            self.particles.add(self.particleType(self.game, pygame.Vector2(1, 0).rotate(random.randint(self.dirRange[0], self.dirRange[1])), pygame.Vector2(self.entityRect.center), self.particleKwargs))
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

class PlayerParticles(Particles):
    def __init__(self, game, entity):
        self.entity = entity
        super().__init__(game, entity, size = 6, dirRange=(140, 220), tickSpeed=80)
        self.setParticleKwargs(color=colors.rgba(colors.grey, 120), speed=0, size=(15,15), shrink=0.5, life=200)
        self.step = 90

    def update(self):
        self.entityRect = self.entity.rect
        super().update()
  
    def addParticles(self):
        if len(self.particles) < self.size and pygame.time.get_ticks() - self.lastParticle >= self.tickSpeed:
            if self.entity.body.velocity.length > 1:
                dir = pygame.Vector2(self.entity.body.velocity).normalize()

                pos = pygame.Vector2(self.entityRect.center)
                pos += dir.rotate(self.step) * 10
                self.step*=-1
                dir.rotate_ip(random.randint(self.dirRange[0], self.dirRange[1]))
                self.particles.add(self.particleType(self.game, dir, pos, self.particleKwargs))
                self.lastParticle = pygame.time.get_ticks()
 
class CombatParticles(Particles):
    def __init__(self, game, entity):
        self.entity = entity
        super().__init__(game, entity, dirRange=(140, 220), tickSpeed=80, particleType=NumParticle)
        self.partColor = colors.rgba(colors.white, 150)
        self.critColor = colors.yellow
        self.setParticleKwargs(color=self.partColor, speed=2, size=(40,40), shrink=0.3, life=600, groups = game.layer2)
        self.particleType = NumParticle
        self.step = 90

    def update(self):
        self.entityRect = self.entity.rect
        self.particles.update()

    def particle(self, pos, num=0, crit=False):
        partKwargs = self.particleKwargs.copy()
        partKwargs['num'] = num
        partKwargs['color'] = self.critColor if crit else self.partColor
        self.particles.add(self.particleType(self.game, pygame.Vector2(1, 0).rotate(random.randint(self.dirRange[0], self.dirRange[1])), pos, partKwargs))


class Particle(util.Sprite):
    def __init__(self, game, dir, pos, kwargs):
        self.game = game
        self.groups = game.layer1
        #self.alpha = 255
        self.speed = 2.5
        self.drag = 1
        self.shrink = 0.2
        self.life = 600
        self.colorVariation = 100
        self.color = colors.red
        self.size = (10, 10)
        self.dir = dir
        self.pos = pos

        for k, v in kwargs.items():
            self.__dict__[k] = v
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.init = pygame.time.get_ticks()
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.w = self.size[0]
        self.rect.center = self.pos.x, self.pos.y
        self.render()

    def render(self):
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, colors.dark(self.color, random.randint(0, self.colorVariation)), (self.rect.width/2, self.rect.height/2), self.w/2)

    def update(self):
        self.pos += self.dir*self.speed* self.game.dt2()
        self.speed *= self.drag
        self.rect.center = self.pos.x, self.pos.y
        self.w -= self.shrink
        self.render()
        if pygame.time.get_ticks() - self.init >= self.life:
            self.kill()

class NumParticle(Particle):
    def __init__(self, game, dir, pos, kwargs):
        self.num = 0
        self.font = fonts['effect2']
        super().__init__(game, dir, pos, kwargs)
        self.drag = 0.90
        self.shrink = 0

    def render(self):
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(self.font.render(str(self.num), self.game.antialiasing, self.color), (0, 0))
    
    def update(self):
        self.pos += self.dir*self.speed
        self.speed *= self.drag
        self.rect.center = self.pos.x, self.pos.y
        self.render()
        if pygame.time.get_ticks() - self.init >= self.life:
            self.kill()

### This is pretty pointless but eyy
# class highlight(util.Sprite):
#     def __init__(self, game, entity, **kwargs):
#         self.game = game
#         self.groups = game.sprites, game.layer1
#         pygame.sprite.Sprite.__init__(self, self.groups)
        
#         for k, v in kwargs.items():
#             self.__dict__[k] = v
#         self.entity = entity
#         self.entImgRect = pygame.Rect(entity.rect.x, entity.rect.y, self.entity.image.get_width(), self.entity.image.get_height())
#         self.rect = pygame.Rect(self.entImgRect)
#         self.render()

#     def render(self):
#         self.rect.w = self.entImgRect.w*1.2
#         self.rect.h = self.entImgRect.h*1.2
#         self.image = pygame.transform.scale(self.entity.image, (self.rect.w, self.rect.h))
#         self.image.fill((255, 255, 255), special_flags = pygame.BLEND_MAX)
    
#     def update(self):
#         self.entImgRect = pygame.Rect(self.entity.rect.x, self.entity.rect.y, self.entity.image.get_width(), self.entity.image.get_height())
#         self.render()
#         self.rect.center = self.entImgRect.center
