uv run pyinstaller main.py \
    --onefile \
    --name "The Caverns" \
    --noconfirm \
    --add-data assets:assets \
    --hidden-import OpenGL.platform.egl \
    --collect-all pygame_render \
    --collect-all pygame_light2d

# uv run python3 -m nuitka \
#     --enable-plugin=numpy \
#     --onefile \
#     --follow-imports \
#     --include-data-dir=assets=assets \
#     --linux-onefile-icon=assets/logo.jpeg \
#     --disable-console \
#     --show-progress \
#     --show-scons \
#     --show-memory \
#     main.py
