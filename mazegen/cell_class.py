class Cell:
    """
    Represents a single cell in a maze grid.

    Each cell encodes the presence or absence of walls in the four
    cardinal directions (north, east, south, west) using a bitmask
    integer value. Additional flags indicate whether the cell has
    special roles such as being the start, end, part of a path,
    or part of the 42 pattern.

    Wall Encoding:
        The `value` parameter uses bitwise flags:
        - 1 (bit 0): north wall
        - 2 (bit 1): east wall
        - 4 (bit 2): south wall
        - 8 (bit 3): west wall

        A bit set to 1 means the wall is open (i.e., no wall),
        while 0 means the wall is present.

    Attributes:
        north (bool): True if the north wall is open.
        east (bool): True if the east wall is open.
        south (bool): True if the south wall is open.
        west (bool): True if the west wall is open.
        is_start (bool): True if this cell is the maze entry point.
        is_end (bool): True if this cell is the maze exit point.
        is_path (bool): True if this cell is part of a solution path.
        is_ftwo (bool): True if this cell is part of the 42 pattern.

    Methods:
        open_wall(direction: str) -> None:
            Closes a wall in the given direction by setting it to False.

        to_hex() -> str:
            Serializes the cell back into a single hexadecimal character
            representing its wall configuration.
    """
    def __init__(self,
                 value: int = 15,
                 is_start: bool = False,
                 is_end: bool = False,
                 is_path: bool = False,
                 is_ftwo: bool = False):

        # True means wall is open
        self.north: bool = bool(value & 1)
        self.east: bool = bool(value & 2)
        self.south: bool = bool(value & 4)
        self.west: bool = bool(value & 8)

        self.is_start = is_start
        self.is_end = is_end
        self.is_path = is_path
        self.is_ftwo = is_ftwo
        if is_path:
            self.next_block = ""

    def open_wall(self, direction: str) -> None:
        """(remove) a wall by name: 'north', 'east', 'south', 'west'."""
        setattr(self, direction, False)

    def to_hex(self) -> str:
        """Serialize back to a single hex character for the output file."""
        value = (self.north * 1
                 + self.east * 2
                 + self.south * 4
                 + self.west * 8)
        return format(abs(15-value), 'X')
