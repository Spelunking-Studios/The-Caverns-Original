import pygame
from stgs import *
import util 

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
    lifespan = 1000

    def __init__(self, game):
        self.game = game
        super().__init__(self, (game.sprites, game.layer2))

        self.particles = []
        self.start_time = now()

    def update(self):
        if now() - self.start_time >= self.lifespan:
            self.kill()
        else:
            self.step()
            self.add_particle()

    def step(self):
        for p in self.particles:
            p[2] *= 0.97 # Decrease size
            p[1] += p[4] # Add Velocity Y
            p[0] += p[3] # Add Velocity X
            p[4] += 0.3  # Add acceleration
            if p[1] >= HEIGHT:
                self.particles.remove(p)
    
    def add_particle(self):
        self.particles.append([0, 0, 0, 0, 0])

    def draw(self, surf, transform=None):
        for p in self.particles:
            pygame.draw.circle(surf, (255, 255, 255), (p[0], p[1]), p[3])

class GlowParticles(ParticleController):
    """Glowing particles that fall to the bottom of the screen
    """

    def __init__(self, game, position=(0, 0)):
        super().__init__(game)
        self.position = position
        self.particle_size = 5
        self.color = (255, 255, 255)
        self.glow_brightness = 20

    def update_position(self, new=(0,0)):
        self.position = new

    def add_particle(self):
        self.particles.append([ self.position[0], 
                                self.position[1], 
                                self.particle_size,
                                (random.random()-0.5)*3,
                                -(random.random())*5
                              ])

    def step(self):
        for p in self.particles:
            p[2] *= 0.97 # Decrease size
            p[1] += p[4] # Add Velocity Y
            p[0] += p[3] # Add Velocity X
            p[4] += 0.3  # Add acceleration
            if p[1] >= HEIGHT:
                self.particles.remove(p)
    @staticmethod
    def glow_surface(radius, color):
        surf = pygame.Surface((int(radius*2), int(radius*2)))
        pygame.draw.circle(surf, color, (radius, radius),radius)
        surf.set_colorkey((0,0,0))

        return surf
    
    def draw(self, surf, transform = lambda x: x):
        for p in self.particles:
            pygame.draw.circle(surf, self.color, (p[0], p[1]), p[2])
            
            # Glow Effect
            r = p[2]*2
            
            surf.blit(self.glow_surface( 
                        r, 
                        (self.glow_brightness, self.glow_brightness, self.glow_brightness) 
                     ),
                     transform( (p[0]-r, p[1]-r) ),
                     special_flags = pygame.BLEND_RGB_ADD
                    )
            
