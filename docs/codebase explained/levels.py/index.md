# levels.py

## class Room

Represents a single room within the game.

### properties

#### roomFilePath

A string containing the path to the room Tiled file (the  `.tmx` filed to load).

Type: `str`

#### scale

Represents the scale at which the room is drawn. A scale of 1 (the default) draws the room at the exact size of the room. A scale greater than 1 draws the room at the size: $[width, height] * scale$

Type: `int`
Default: `1`
