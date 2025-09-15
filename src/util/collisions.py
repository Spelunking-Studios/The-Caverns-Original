PLAYER_GROUP = 1

class Handler:
    """Object to handle collision interactions

    collision groups:

    1 - Walls
    2 - Player
    3 - Player Projectiles
    4 - Enemies
    5 - Enemy Projectiles
    6 - Shield

    This is going to be different than the weapon collisions and 
    projectile on enemy collisions which will instead use 
    collision masks for pixel perfect collisions.

    This integrates with the physics engine
    """
    def __init__(self, game):
        self.game = game
        self.space = game.space

        self.create_handlers()
        self.create_filters()

    def create_handlers(self):
        # set up collision handlers here
        # use collision groups in docstring

        player_projectile_hit_walls = self.space.add_collision_handler(1, 3)
        player_projectile_hit_walls.begin = kill

        enemy_projectile_hit_walls = self.space.add_collision_handler(1, 5)
        enemy_projectile_hit_walls.begin = kill

        enemy_projectile_hit_walls = self.space.add_collision_handler(5, 6)
        enemy_projectile_hit_walls.begin = kill

        projectiles_hit_enemies = self.space.add_collision_handler(4, 3)
        projectiles_hit_enemies.begin = hit_enemy

        projectiles_hit_player = self.space.add_collision_handler(2, 5)
        projectiles_hit_player.begin = hit_player

    def create_filters(self):
        # Make collision exclude each other here
        pass



def kill(arbiter, space, data):
    for shape in arbiter.shapes:
        if shape.collision_type != 1:
            shape.body.owner.kill()
            return False
    
    return True

def hit_enemy(arbiter, space, data):
    projectile, enemy = None, None

    for shape in arbiter.shapes:
        if shape.collision_type == 3:
            projectile = shape.body.owner

        if shape.collision_type == 4:
            enemy = shape.body.owner
    if enemy:
        projectile.hit(enemy)
        return True
    else:
        return False

def hit_player(arbiter, space, data):
    projectile, player = None, None

    for shape in arbiter.shapes:
        if shape.collision_type == 5:
            projectile = shape.body.owner

        if shape.collision_type == 2:
            player = shape.body.owner

    projectile.hit(player)
    return True
