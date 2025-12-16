import pygame, pymunk
from pygame.math import Vector2 as Vec
import math
from .enemy import SimpleEnemy
from src import util
from src.util import print_stats
from src.util.fabrik import fabrik
from src.stgs import *
from src.animations import Animator
from src.util import print_stats


class GrabPlant(SimpleEnemy):
    challenge_rating = 1

    head_open = pygame.image.load(asset("enemies/grab_plant.png"))
    head_closed = pygame.image.load(asset("enemies/grab_plant.png"))

    def __init__(self, game, objT):
        super().__init__(game, objT)
        
        self.state = "hide"
        self.last_attack = 0
        self.pause = 0

        self.pos = Vec(objT.x, objT.y)
        self.set_stats()
        self.make_body()

        for p in self.points:
            p += self.pos

        self.rect.center = (objT.x, objT.y)

        self.animation = Animator({
            "open": self.head_open,
            "closed": self.head_closed
        }, 90, mode = "open")
        self.hidden = False
        self.thickness_delta = (self.thickness_max-self.thickness_min)/(len(self.points)-1)

    @print_stats
    def set_stats(self):
        self.length = 20
        self.segment_length = 10
        self.speed = 11
        self.chomp_dist = 10
        self.pull_speed = 30000
        self.damage = 3
        self.health = 200

        self.attack_delay = 300

    def make_body(self):
        self.color = (0, 0, 0)
        self.thickness_min = 5
        self.thickness_max = 15
        self.points = [Vec(0, self.segment_length*i) for i in range(self.length+1)]
        
        self.rect = self.head_open.get_rect()
        self.create_physics(2, self.chomp_dist, self.move_physics_body)
    
    def update(self):
        super().update()
        self.animation.update()
        self.check_state()

        if self.hidden:
            self.body.owner = None
        else:
            self.body.owner = self

    def check_state(self):
        pos = tuple(self.points[0])
        head = tuple(self.points[-1])
        match self.state:
            case "searching":
                # Looks to see if player is within reach
                if util.distance(pos, self.game.player.rect.center) < self.length*self.segment_length-self.chomp_dist:
                    self.state = "chase"
            case "chase":
                self.hidden = False
                if util.distance(pos, self.game.player.rect.center) > self.length*self.segment_length:
                    self.state = "hide"
                else:
                    if util.distance(head, self.game.player.rect.center) <= self.chomp_dist:
                        self.state = "grabbed" 
                    else:
                        self.move_to_position(self.game.player.rect.center)
            case "hide":
                if util.distance(pos, head) < self.speed + 0.2:
                    self.hidden = True
                    self.state = "searching"
                else:
                    self.hide_in_hole()
            case "grabbed":
                if util.distance(head, self.game.player.rect.center) > self.chomp_dist:
                    self.state = "chase"
                else:
                    self.pull_player()
                    self.attack()
                    # self.move_to_position(self.game.player.rect.center)

    def move_to_position(self, position):
        head_position = self.points[-1].copy()
        target = Vec(position)
        diff = target-head_position
        diff.clamp_magnitude_ip(0, self.speed)
        fabrik(self.points, head_position + diff)
        # fabrik(self.points, head_position)

    def hide_in_hole(self):
        self.move_to_position(self.points[0].copy())

    def pull_player(self):
        target = self.game.player.body
        diff = self.points[0]-tuple(target.position)
        diff.clamp_magnitude_ip(self.pull_speed, self.pull_speed+10)
        target.apply_impulse_at_local_point(tuple(diff), (0, 0))
        target.apply_force_at_local_point(tuple(diff), (0, 0))

    def attack(self):
        if now() - self.last_attack > self.attack_delay:
            self.game.player.take_damage(self.damage)

    def rotated_head(self):
        angle_vec = self.points[-1] - self.game.player.rect.center
        img = pygame.transform.rotate(self.animation.get_image(), -1*angle_vec.angle-90)
        self.rect = img.get_rect(center=self.points[-1].copy())
        self.image = img
        return img
    
    def move_physics_body(self, body, *args):
        body.position = self.rect.center

    def take_damage(self, dmg):
        super().take_damage(dmg)

    def draw(self, ctx, transform=None):
        if not self.hidden:
            thickness = self.thickness_max
            for i in range(1, len(self.points)):
                prev = pygame.Rect(*self.points[i-1], 1, 1)
                cur = pygame.Rect(*self.points[i], 1, 1)
                pygame.draw.line(ctx, self.color, transform(prev).topleft, transform(cur).topleft, int(thickness))
                thickness -= self.thickness_delta

            ctx.blit(self.rotated_head(), transform(self.rect))
