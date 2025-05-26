class Handler:
    """Object to handle collision interactions

    collision groups:

    1 - Walls
    2 - Player
    3 - Projectiles
    4 - Enemies

    This is going to be different than the weapon collisions and 
    projectile on enemy collisions which will instead use 
    collision masks for pixel perfect collisions.

    This integrates with the physics engine
    """
    def __init__(self, game):
        self.game = game
        self.space = game.space

        self.create_handlers()

    def create_handlers(self):
        # set up collision handlers here
        # use collision groups in docstring

        projectile_hit_walls = self.space.add_collision_handler(1, 3)
        projectile_hit_walls.begin = kill



def kill(arbiter, space, data):
    for shape in arbiter.shapes:
        if shape.collision_type == 3:
            shape.body.owner.kill()
            return False
    
    return True
