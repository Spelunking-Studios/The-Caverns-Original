import pygame
import random
from pygame import Vector2 as Vec
from src.stgs import *
from src import util
from src.util import LightEffect

class ParticleController(util.Sprite):
    """A basic class that controls a set of particles designed
    to be optimized with arrays 

    When making your own particles look at redefining
    * step()
    * draw()
    And updating
    * speed
    * lifespan

    If you choose to use an image for a particle, please bake
    it before hand (store it in memory)
    """

    batch_size = 0
    lifespan = 100000

    def __init__(self, game):
        self.game = game
        super().__init__((game.sprites, game.groups.particle_emitters, game.layer3))

        self.particles = []
        self.position = (0, 0)
        self.start_time = now()
        self.color = (255, 255, 255)

    def update(self):
        if now() - self.start_time >= self.lifespan:
            self.kill()
        else:
            self.step()
            self.add_particle()

    def update_position(self, new):
        self.position = new

    def step(self):
        for p in self.particles:
            p[2] *= 0.97 # Decrease size
            p[1] += p[4] # Add Velocity Y
            p[0] += p[3] # Add Velocity X
            p[4] += 0.03  # Add acceleration
            if p[1] >= winHeight:
                self.particles.remove(p)
    
    def add_particle(self):
        self.particles.append([0, 0, 0, 0, 0])

    def get_batch_size(self):
        return len(self.particles)

    def draw(self, surf, transform=None):
        x, y = self.position
        for p in self.particles:
            pygame.draw.circle(surf, self.color, (p[0] + x, p[1] + y), p[2])



class GlowParticles(ParticleController):
    """Glowing particles that fall to the bottom of the screen
    """

    def __init__(self, game, **kwargs):
        super().__init__(game)
        self.position = (0, 0)
        self.particle_size = 5
        self.color = (255, 255, 255)
        self.glow_brightness = 0.3 
        self.speed = 3
        self.on_finish = None

        self.dump(kwargs)


    def add_particle(self):
        x, y = self.position
        self.particles.append([ x, 
                                y, 
                                self.particle_size,
                                (random.random()-0.5)*self.speed,
                                (random.random()-0.5)*self.speed,
                                self.color
                              ])

    @staticmethod
    def glow_surface(radius, color):
        surf = pygame.Surface((int(radius*2), int(radius*2)))
        pygame.draw.circle(surf, color, (radius, radius),radius)
        surf.set_colorkey((0,0,0))

        return surf
    
    def draw(self, surf, transform = lambda x: x):
        #optional offset
        x, y = 0, 0
        transform = self.game.cam.applyTuple
        for p in self.particles:
            pygame.draw.circle(surf, p[5], transform((p[0] + x, p[1] + y)), p[2])
            
            # Glow Effect
            r = p[2]*2
            
            surf.blit(self.glow_surface( 
                        r, 
                        (int(p[5][0]*self.glow_brightness), int(p[5][1]*self.glow_brightness), int(p[5][2]*self.glow_brightness))
                     ),
                     transform( (p[0] + x - r, p[1] + y - r) ),
                     special_flags = pygame.BLEND_RGB_ADD
                    )
class FlameParticles(GlowParticles):
    def __init__(self, game):
        super().__init__(game)

    def step(self):
        for p in self.particles:
            p[2] += 0.2 # increase size
            p[1] += p[4] # Add Velocity Y
            p[0] += p[3] # Add Velocity X
            p[4] += 0.0  # Add acceleration
            p[5] = util.dark(p[5], 1) # Color
            p[6] += 1 # Lifespan
            if p[1] >= winHeight or p[6] > 100:
                self.particles.remove(p)
    
    def add_particle(self):
        self.particles.append([0, 0, 1, random.random()-0.5, random.random()-0.5, util.peach_rose, 3])

class SlowGlowParticles(GlowParticles):
    def __init__(self, game, **kwargs):
        self.last_particle = 0
        self.bright = False
        self.brightness = 0.8
        self.speed = 2
        super().__init__(game)
        self.particle_size = 5
        self.delay = 70
        self.dump(kwargs)

    def update(self):
        self.step()
        if now() - self.start_time >= self.lifespan:
            if self.on_finish:
                self.on_finish()
                self.on_finish = None
            if now() - self.start_time >= self.lifespan*2:
                self.kill()
        else:
            if now() - self.last_particle > self.delay:
                self.add_particle()
                self.last_particle = now()

    def step(self):
        for p in self.particles:
            p[2] = max(p[2]-0.01, 0) # increase size
            p[1] += p[4] # Add Velocity Y
            p[0] += p[3] # Add Velocity X
            p[4] += 0.0  # Add acceleration
            p[5] = util.dark(p[5], 1) # Color
            p[6].power = p[2]*0.15
            p[6].pos = (p[0], p[1])
            p[7] += 1
            if p[7] > 100 or p[2] <= 0:
                # p[6].kill()
                self.particles.remove(p)
    
    def add_particle(self):
        x, y = self.position
        self.particles.append([ x, 
                                y, 
                                self.particle_size,
                                (random.random()-0.5)*self.speed,
                                (random.random()-0.5)*self.speed,
                                self.color,
                                LightEffect(self.game, pygame.Rect(0, 0, 10, 10), power=self.brightness, radius=50, color=self.color), 
                                0
                              ])

    def draw(self, surf, transform = lambda x: x):
        transform = self.game.cam.applyTuple
        x, y = 0, 0#self.position
        for p in self.particles:
            # print(transform((p[0] + x, p[1] + y)))
            # print(p[5])
            pygame.draw.circle(surf, p[5], transform((p[0] + x, p[1] + y)), p[2])
            
            if self.bright:
                # Glow Effect
                r = p[2]*2
                
                surf.blit(self.glow_surface( 
                            r, 
                            (int(p[5][0]*self.glow_brightness), int(p[5][1]*self.glow_brightness), int(p[5][2]*self.glow_brightness))
                         ),
                         transform( (p[0] + x - r, p[1] + y - r) ),
                         special_flags = pygame.BLEND_RGB_ADD
                        )

