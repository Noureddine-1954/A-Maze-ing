import sys
from typing import Dict, Any


class ConfigError(Exception):
    """Exception raised for invalid or missing maze configuration values.

    Used throughout the parsing pipeline to signal any error that prevents
    the program from constructing a valid :class:`MazeGenerator` configuration,
    including malformed config files, out-of-bounds coordinates, and
    unsatisfied required keys.
    """

    pass


def ftwo_cells(height: int, width: int) -> set[tuple[int, int]]:
    """Return the set of grid coordinates occupied by the ``42`` pattern.

    Computes the cells that form the digit glyphs ``4`` and ``2``, each
    rendered as a 5x5 pixel bitmap, centred horizontally and vertically in a
    maze of the given dimensions. If the maze is too small to fit the pattern,
    an empty set is returned instead.

    The ``4`` glyph occupies columns ``offset`` to ``offset + 4`` and the
    ``2`` glyph occupies columns ``offset + 5`` to ``offset + 9``, where
    ``offset = width // 2 - 5``. Both glyphs share the same row offset of
    ``height // 2 - 2``.

    Args:
        height: Number of rows in the maze grid.
        width: Number of columns in the maze grid.

    Returns:
        A set of ``(row, col)`` tuples for every cell that belongs to the
        ``42`` pattern, or an empty set if ``width < 10`` or ``height < 7``.
    """
    if width < 10 or height < 7:
        return set()

    four = [
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ]
    two = [
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
    ]

    row_offset = height // 2 - 2
    col_offset = width // 2 - 5
    cells = set()

    for r, row in enumerate(four):
        for c, val in enumerate(row):
            if val:
                cells.add((row_offset + r, col_offset + c))

    for r, row in enumerate(two):
        for c, val in enumerate(row):
            if val:
                cells.add((row_offset + r, col_offset + 5 + c))

    return cells


def parse_pair(value: str) -> tuple[int, int]:
    """Parse a ``"row, col"`` string into an integer coordinate tuple.

    Expects exactly two comma-separated integer tokens. Leading and trailing
    whitespace around each token is ignored.

    Args:
        value: A string of the form ``"row, col"`` (e.g. ``"3, 7"``).

    Returns:
        A ``(row, col)`` tuple of integers.

    Raises:
        ConfigError: If ``value`` does not contain exactly one comma, or if
            either token cannot be converted to an integer.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"Invalid coordinate format: {value}")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ConfigError(f"Invalid coordinate numbers: {value}")


def ft_parsing() -> Dict[str, Any]:
    """Parse and validate the maze config file supplied on the command line.

    Reads the plain-text config file passed as ``sys.argv[1]``, parses each
    ``KEY = VALUE`` directive, and validates the combined configuration before
    returning it. Blank lines and lines beginning with ``#`` are ignored.

    The following keys are **required**:

    - ``WIDTH`` — positive integer number of maze columns.
    - ``HEIGHT`` — positive integer number of maze rows.
    - ``ENTRY`` — ``"row, col"`` coordinate of the maze entry point.
    - ``EXIT`` — ``"row, col"`` coordinate of the maze exit point.
    - ``OUTPUT_FILE`` — path to the file where the solved maze is written.
    - ``PERFECT`` — ``True`` or ``False``; whether to generate a perfect maze.

    The following key is **optional**:

    - ``SEED`` — integer random seed for reproducible maze generation.
      Defaults to ``None`` when omitted.

    Cross-field validation enforced after parsing:

    - ``ENTRY`` and ``EXIT`` must differ.
    - Both coordinates must lie within the ``HEIGHT x WIDTH`` grid bounds.
    - Neither ``ENTRY`` nor ``EXIT`` may overlap the embedded ``42`` pattern
      (see :func:`ftwo_cells`).
    - ``OUTPUT_FILE`` must be writable.

    Returns:
        A dictionary mapping each recognised key to its parsed Python value.
        ``SEED`` is always present; it is ``None`` when not specified in the
        config file.

    Raises:
        ConfigError: If the program is not invoked with exactly one argument,
            if the config file cannot be read, if any key is duplicated,
            unknown, or malformed, if required keys are absent, or if any
            cross-field validation rule is violated.
    """
    if len(sys.argv) != 2:
        msg = "Invalid usage, program must be run with the following command: "
        raise ConfigError(msg + "python3 a_maze_ing.py config.txt")

    config_content: Dict[str, Any] = {}
    required = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

    try:
        with open(sys.argv[1]) as config_file:
            for line in config_file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Bad line: {line}")

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key in config_content:
                    raise ConfigError(f"{key} was declared more than once")

                if key == "WIDTH":
                    try:
                        config_content[key] = int(value)
                    except ValueError:
                        raise ConfigError(f"{key} must be an integer")

                elif key == "HEIGHT":
                    try:
                        config_content[key] = int(value)
                    except ValueError:
                        raise ConfigError(f"{key} must be an integer")

                elif key == "ENTRY":
                    config_content[key] = parse_pair(value)

                elif key == "EXIT":
                    config_content[key] = parse_pair(value)

                elif key == "OUTPUT_FILE":
                    config_content[key] = value

                elif key == "PERFECT":
                    if value.lower() == "true":
                        config_content[key] = True
                    elif value.lower() == "false":
                        config_content[key] = False
                    else:
                        msg = f"Invalid argument for {key}: {value}"
                        raise ConfigError(msg + " expected True/False")

                elif key == "SEED":
                    try:
                        config_content[key] = int(value)
                    except ValueError:
                        raise ConfigError("Given Seed is not a valid int")

                else:
                    raise ConfigError(f"Unknown key: {key}")

    except (FileNotFoundError, PermissionError) as e:
        raise ConfigError(e)

    missing = required - config_content.keys()
    if missing:
        raise ConfigError(f"Missing keys: {missing}")

    if config_content["ENTRY"] == config_content["EXIT"]:
        raise ConfigError("ENTRY and EXIT cannot be the same")

    width = config_content["WIDTH"]
    height = config_content["HEIGHT"]
    entry_x, entry_y = config_content["ENTRY"]
    exit_x, exit_y = config_content["EXIT"]

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be > 0")

    if not (0 <= entry_y < width and 0 <= entry_x < height):
        raise ConfigError("ENTRY outside maze bounds")

    if not (0 <= exit_y < width and 0 <= exit_x < height):
        raise ConfigError("EXIT outside maze bounds")

    if "SEED" not in config_content:
        config_content["SEED"] = None

    ftwo = ftwo_cells(config_content["HEIGHT"], config_content["WIDTH"])
    if config_content["ENTRY"] in ftwo:
        raise ConfigError("ENTRY cannot be inside the 42 pattern")
    if config_content["EXIT"] in ftwo:
        raise ConfigError("EXIT cannot be inside the 42 pattern")

    try:
        fichier = open(config_content['OUTPUT_FILE'], 'w')
        fichier.close()

    except Exception as e:
        raise ConfigError(e)

    return config_content
