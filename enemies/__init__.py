from .eBullet import *
from .enemy import *
from .goblin import *
from .tormentor import *


# import os
# import importlib

# dir_path = os.path.join(os.getcwd(), 'sprites', '__init__.py')
# print(dir_path)

# __all__ = []
# for file in os.listdir(dir_path):
#     if file.endswith(".py") and file != "__init__.py":
#         __all__.append(file[:-3])
#         if __name__ == "__main__":
#             print(f'Loaded: {file[:-3]}')
#             importlib.import_module(file[:-3])
#         else:
#             importlib.import_module(f"{os.path.basename(os.path.split(__file__)[0])}.{file[:-3]}")
