@REM Attach mode is needed for the console mode in order to not trigger Windows Defender
uv run nuitka ^
    --mode=standalone ^
    --include-data-dir=assets=assets ^
    --include-data-files=./.venv/Lib/site-packages/pygame/libpng16-16.dll=libpng16-16.dll ^
    --include-data-files=./.venv/Lib/site-packages/pygame/libjpeg-62.dll=libjpeg-62.dll ^
    --lto=yes ^
    --jobs=18 ^
    --windows-company-name="Spelunking Studios" ^
    --windows-product-name="The Caverns" ^
    --windows-file-version="0.0.1" ^
    --windows-product-version="0.0.1" ^
    --windows-file-description="A top down indie action-adventure RPG" ^
    --windows-console-mode="attach" ^
    main.py