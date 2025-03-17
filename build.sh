python3 -m nuitka \
    --enable-plugin=numpy \
    --onefile \
    --follow-imports \
    --include-data-dir=assets=assets \
    --linux-onefile-icon=assets/logo.jpeg \
    --disable-console \
    --show-progress \
    --show-scons \
    --show-memory \
    main.py