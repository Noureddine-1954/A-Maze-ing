import sys
from typing import Dict, Any


class ConfigError(Exception):
    """Custom Error"""
    pass


def ftwo_cells(height: int, width: int) -> set[tuple[int, int]]:
    """abgherbvj"""
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
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"Invalid coordinate format: {value}")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ConfigError(f"Invalid coordinate numbers: {value}")


def ft_parsing() -> Dict[str, Any]:

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

                # check for duplicate configs
                if key in config_content:
                    raise ConfigError(f"{key} was declared more than once")

                # check for each of the 5 mandatory and the seed key
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

    except (FileNotFoundError, PermissionError):
        # check if config.txt exists or have permission
        raise ConfigError(f"{sys.argv[1]}, not found")
    # check wether all requirements are met
    missing = required - config_content.keys()
    if missing:
        raise ConfigError(f"Missing keys: {missing}")

    # check if entry and exit are the same
    if config_content["ENTRY"] == config_content["EXIT"]:
        raise ConfigError("ENTRY and EXIT cannot be the same")

    # check for the logic of the coordinates and the size of the maze
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

    # in case additional keys were not given
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

    # print(config_content)
    return config_content
