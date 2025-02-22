python3 -m nuitka \
    --enable-plugin=numpy \
    --onefile \
    --follow-imports \
    --include-data-dir=assets=assets \
    --linux-onefile-icon=assets/logo.jpeg \
    --macos-app-icon=assets/logo.jpeg \
    --macos-signed-app-name="com.spelunking-studios.the-caverns" \
    --macos-app-name="The Caverns" \
    --macos-app-version="0.0.1" \
    --macos-disable-console \
    --show-progress \
    --show-scons \
    --show-memory \
    main.py