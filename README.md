# 𝕿𝖍𝖊 𝕮𝖆𝖛𝖊𝖗𝖓𝖘   
### A Pygame Game

An exploration ARPG with fantasy D&D elements.

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

## Building with Nuitka

Make sure you have nuitka installed in uv's virtual environment:

```
uv sync
```

Then run nuitka:

```
uv run nuitka --mode=standalone --include-data-dir=assets=assets --lto=no main.py
```

The generated stuff is in `main.dist`. For now, the entire folder needs to be copied to test it.
If possible, perhaps exploring the `--mode=onefile` option would help.
