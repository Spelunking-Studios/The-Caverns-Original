class Handler:
    def __init__(self, game):
        self.game = game
        self.space = game.space

        self.create_handlers()

    def create_handlers(self):
        projectile_hit_walls = self.space.add_collision_handler(1, 3)
        projectile_hit_walls.begin = kill



def kill(arbiter, space, data):
    for shape in arbiter.shapes:
        if shape.collision_type == 3:
            shape.body.owner.kill()
            return False
    
    return True
