import pygame
from src import util
import src.util.colors as colors
import math
from src import fx
from src.stgs import asset
from .lights import LightSource, LightEffect
from src.animations import BasicAnimation


class Projectile(util.Sprite):
    def __init__(self, game, pos, target, **kwargs):
        self.groups = game.sprites, game.layer2
        self.game = game
        self.offset = 0
        self.vel = 10

        self.dump(kwargs)

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

    def hit(self, enemy=None):
        dmg = self.game.player.stats.attack()
        if enemy:
            enemy.take_damage(dmg[0])
            self.game.player.combatParts.particle(self.pos, dmg[0], dmg[1])

        self.kill()


class Fireball(Projectile):
    light_img = pygame.image.load(asset("objects/light1.png"))
    def __init__(self, game):
        mPos = game.get_mouse_pos() - pygame.Vector2(game.cam.apply(game.player).center)
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
        self.light = LightSource(game, self.rect, source_img=self.light_img, default_size=True)

        self.create_physics(5, 4, self.fake_move)

    def fake_move(self, body, *args):
        body.position = tuple(self.pos)

    def update(self):
        super().update()
        self.light.rect.center = self.rect.center
        self.animations.update()

    def kill(self):
        super().kill()
        self.particles.setLife(220)
        LightEffect(self.game, self.rect, source_img=self.light_img, default_size=True, lifespan=220)
        self.light.kill()

class ThrowingKnife(Projectile):
    def __init__(self, game):
        mPos = game.get_mouse_pos() - pygame.Vector2(game.cam.apply(game.player).center)
        super().__init__(
            game,
            game.player.rect.center,
            mPos,
            groups=(game.sprites, game.layer2, game.groups.pProjectiles)
        )
        self.imgSheet = {'main': asset('player/knife.png')}
        try:
            angle = math.degrees(math.atan2(-mPos.y, mPos.x))
        except ValueError:
            angle = 0
        self.animations = BasicAnimation(self, angle = angle-90)
        self.image = self.animations.getFirstFrame()
        self.animations.rotate_center()

        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
        # self.particles = fx.Particles(self.game, self.rect, tickSpeed=20, size=8)
        # self.particles.setParticleKwargs(speed=1.2, shrink=0.4, life=100, color=colors.orangeRed)
        self.light = LightSource(game, self.rect, img=asset("objects/light1.png"))

        self.create_physics(5, 4, self.fake_move)
        
        self.lifespan = 600
        self.created = now()

    def fake_move(self, body, *args):
        body.position = tuple(self.pos)

    def update(self):
        super().update()
        self.light.rect.center = self.rect.center
        if now() - self.created >= self.lifespan:
            self.kill()
        # self.animations.update()

    def kill(self):
        # Play sound
        super().kill()
        # LightEffet(self.game, self.rect)
        self.light.kill()
