import os

command = f'pyinstaller main.py --noconfirm --onefile --icon="logo.ico" --add-data "assets;assets/" --add-data "fonts;fonts/"'
print(command)
os.system(command)