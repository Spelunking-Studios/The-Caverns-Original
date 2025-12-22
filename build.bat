uv run pyinstaller main.py ^
    --onefile ^
    --name "The Caverns" ^
    --noconfirm ^
    --add-data assets:assets ^
    --hidden-import OpenGL.platform.egl ^
    --collect-all pygame_render ^
    --collect-all pygame_light2d
cd packaging\windows
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" msi.iss
