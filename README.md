# 𝕿𝖍𝖊 𝕮𝖆𝖛𝖊𝖗𝖓𝖘   
### A Pygame Game

A top down dungeon crawler ARPG with loadout options and terrifying creatures

Uses Tiled level designer.
https://www.mapeditor.org/

> * python 3.13+
> * pygame 2.0.1
> * PyTMX 3.30

## Usage

Make sure the packages are installed.
```bash
uv sync
```

and simply run the main file.

```bash
uv run main.py
```

## Building to an Executable

Make sure you have nuitka installed in uv's virtual environment:

```
uv sync
```

Then use the build script for your operating system:

```
# Windows
.\build.bat

# Linux
./build.sh
```

The compiled output is located in the `main.dist` folder with intermediary build artifacts in `main.build`.

## Generating a Microsoft Installer

1. Make sure you have [Inno Setup](https://jrsoftware.org/isinfo.php) installed
2. In a termianl, cd to the root of the project
3. Run `iscc .\the-caverns-installer.iss`
4. The generated installer file will be in the `dist` folder
