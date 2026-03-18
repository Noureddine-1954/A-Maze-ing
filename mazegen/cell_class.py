class Cell:
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
