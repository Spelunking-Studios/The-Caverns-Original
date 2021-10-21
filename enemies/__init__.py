from .ankheg import *
from .eBullet import *
from .enemy import *
from .zombie import *


# import os

# dir_path = os.path.join(os.path.dirname(__file__))
# print(dir_path)

# for file in os.listdir(dir_path):
#     if file.endswith(".py") and file != "__init__.py":
#         x = __import__('enemies.'+file[:-3], globals(), locals(), [], 0)
#         for k, v in x.__dict__.items():
#             print(k)
