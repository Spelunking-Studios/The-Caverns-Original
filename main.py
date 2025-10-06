import os
from src.game import Game

if __name__ == '__main__':
    game = Game()

    if os.environ.get("ENABLE_PROFILES", False):
        import cProfile
        cProfile.run("game.run()", filename="game.prof", sort="cumtime")
    else:
        game.run()
