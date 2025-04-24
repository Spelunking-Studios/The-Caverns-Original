import pygame
import util
import src.util.colors as colors
import math
import fx
from stgs import asset
from .lights import LightSource, LightEffect
from animations import BasicAnimation


class Projectile(util.Sprite):
    def __init__(self, game, pos, target, **kwargs):
        self.groups = game.sprites, game.layer2
        self.game = game
        self.offset = 0
        self.vel = 10
        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(asset("player/s1.png"))

        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(target).normalize()
        self.dir = self.dir.rotate(self.offset)
        self.image = pygame.transform.rotate(
            self.image,
            math.degrees(math.atan2(-target.y, target.x)) - self.offset - 135
        )
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
        # fx.Particles(self.game, self.rect, lifeSpan = 100, tickSpeed=20, size = 8)
        #     .setParticleKwargs(speed=1.5, shrink=0.4, life=140, color=colors.orangeRed)

    def create_physics(self, mass, radius, vel_func = None, pos = (0, 0)):
        super().create_physics(mass, radius, vel_func, pos)
        self.shape.sensor = True
        self.shape.collision_type = 3

    def update(self):
        self.pos += self.dir * self.vel * self.game.dt() * 60
        self.rect.center = self.pos
        for e in self.game.groups.getProximitySprites(self, 600, self.game.groups.enemies):
            if hasattr(e, 'image'):
                if pygame.sprite.collide_mask(self, e):
                    self.hit(e)
                    break

    def move(self):
        self.pos += self.dir * self.vel * self.game.dt() * 60
        self.rect.center = self.pos
        pass

    def hit(self, enemy=None):
        dmg = self.game.player.stats.attack()
        if enemy is not None:
            enemy.take_damage(dmg[0])
            self.game.player.combatParts.particle(self.pos, dmg[0], dmg[1])

        self.kill()


class Fireball(Projectile):
    def __init__(self, game):
        mPos = pygame.Vector2(game.get_mouse_pos()) - pygame.Vector2(game.cam.apply(game.player).center)
        super().__init__(
            game,
            game.player.rect.center,
            mPos,
            groups=(game.sprites, game.layer2, game.groups.pProjectiles)
        )
        self.imgSheet = {'main': asset('player/fireball.png')}
        self.animations = BasicAnimation(self)
        self.animations.delay = 30
        self.image = self.animations.getFirstFrame()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
        self.particles = fx.Particles(self.game, self.rect, tickSpeed=20, size=8)
        self.particles.setParticleKwargs(speed=1.2, shrink=0.4, life=100, color=colors.orangeRed)
        self.light = LightSource(game, self.rect, img=asset("objects/light1.png"))

        self.create_physics(5, 4, self.fake_move)

    def fake_move(self, body, *args):
        body.position = tuple(self.pos)


    def update(self):
        super().update()
        self.light.rect.center = self.rect.center
        self.animations.update()

    def kill(self):
        print("killed")
        super().kill()
        self.particles.setLife(220)
        LightEffect(self.game, self.rect)
        self.light.kill()
