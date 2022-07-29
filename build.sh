#! /bin/bash
pyinstaller main.py --onefile --noconfirm --add-data="assets:assets" --add-data="fonts:fonts"