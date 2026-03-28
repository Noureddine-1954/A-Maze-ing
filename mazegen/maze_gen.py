from typing import Optional, Tuple
from collections import deque
from time import time

"""
Maze Generator Module
======================

This module provides the `MazeGenerator` class for generating 2D mazes using a
randomized depth-first search (DFS) algorithm. It supports both perfect mazes
(no cycles) and imperfect mazes (with loops), and can optionally embed a
predefined "42" pattern in the centre. The module also includes a BFS-based
solver to find the shortest path from entrance to exit.

Example:
    >>> from mazegen import MazeGenerator
    >>>
    >>> # Create a 20x20 perfect maze with a fixed seed
    >>> gen = MazeGenerator(height=20, width=20,
    ...                      entrance=(0,0), departure=(19,19),
    ...                      seed=42, perfect=True)
    >>> maze = gen.generate_maze()
    >>>
    >>> # Solve the maze
    >>> path = gen.maze_solver()
    >>>
    >>> # Access the grid
    >>> cell = maze[5][5]
    >>> print(cell.east)   # True if east wall is open
"""


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


class MazeGenerator:
    """
    Generates a 2D maze grid using a depth-first search (DFS) algorithm.

    The maze consists of `Cell` objects arranged in a rectangular grid.
    The generator supports both perfect mazes (no cycles, exactly one path
    between any two points) and imperfect mazes (with loops). It can also
    optionally embed a predefined "42 pattern" inside the maze when the
    dimensions allow it.

    The generation process works as follows:
        1. Initialize a grid of fully closed cells.
        2. Mark entrance and exit cells.
        3. Optionally carve a fixed "42 pattern" in the center.
        4. Use a randomized DFS (backtracking) algorithm to carve passages.
        5. If the maze is not perfect, randomly open additional walls to
           introduce cycles.

    Attributes:
        height (int): Number of rows in the maze.
        width (int): Number of columns in the maze.
        entrance (Tuple[int, int]): Coordinates (row, col) of the entry cell.
        departure (Tuple[int, int]): Coordinates (row, col) of the exit cell.
        seed (Optional[int]): Seed for the random number generator to allow
            reproducible maze generation.
        perfect (bool): If True, generates a perfect maze (no loops).
            If False, introduces random cycles.

    Methods:
        generate_maze() -> list[list[Cell]]:
            Generates and returns the maze as a 2D list of `Cell` objects.
    """
    def __init__(self,
                 height: int,
                 width: int,
                 entrance: Tuple[int, int],
                 departure: Tuple[int, int],
                 seed: Optional[int],
                 perfect: bool):
        self.height = height
        self.width = width
        self.entrance = entrance
        self.departure = departure
        self.seed = seed
        self.perfect = perfect
        self.benchmark = {
            "generation": 0.0,
            "solution": 0.0
        }
        self.gen_maze: list[list[Cell]] = [[]]

    def generate_maze(self) -> list[list[Cell]]:
        start_time = time()
        width = self.width
        height = self.height

        maze = [[Cell(0) for _ in range(width)] for _ in range(height)]

        ent_x, ent_y = self.entrance
        ext_x, ext_y = self.departure
        maze[ent_x][ent_y].is_start = True
        maze[ext_x][ext_y].is_end = True

        def force_ftwo() -> None:
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

            rw_off = height // 2 - 2
            cl_off = width // 2 - 5

            for r, row in enumerate(four):
                for c, val in enumerate(row):
                    if val:
                        if r == 0 and rw_off - 1 >= 0:
                            maze[rw_off - 1][cl_off + c].south = False
                        maze[rw_off + r][cl_off + c - 1].east = False
                        maze[rw_off + r][cl_off + c] = Cell(0)
                        maze[rw_off + r][cl_off + c].is_ftwo = True

            for r, row in enumerate(two):
                for c, val in enumerate(row):
                    if val:
                        if r == 0 and rw_off - 1 >= 0:
                            maze[rw_off - 1][cl_off + 5 + c].south = False
                        maze[rw_off + r][cl_off + 5 + c - 1].east = False
                        maze[rw_off + r][cl_off + 5 + c] = Cell(0)
                        maze[rw_off + r][cl_off + 5 + c].is_ftwo = True

        if not (width < 10 or height < 7):
            force_ftwo()

        def carve() -> None:
            from random import shuffle, seed as set_seed, random

            if self.seed is not None:
                set_seed(self.seed)

            # Directions:
            # (row_delta, col_delta, wall_on_current, wall_on_neighbor)
            dirs = [
                (-1,  0, 'north', 'south'),
                (1,  0, 'south', 'north'),
                (0,  1, 'east',  'west'),
                (0, -1, 'west',  'east'),
            ]

            visited = [[maze[r][c].is_ftwo
                        for c in range(width)] for r in range(height)]

            stack = [(ent_x, ent_y)]
            visited[ent_x][ent_y] = True

            while stack:
                r, c = stack[-1]

                neighbors = [
                    (r + dr, c + dc, cur_wall, nbr_wall)
                    for dr, dc, cur_wall, nbr_wall in dirs
                    if 0 <= r + dr < height
                    and 0 <= c + dc < width
                    and not visited[r + dr][c + dc]
                ]

                if not neighbors:
                    stack.pop()
                    continue

                shuffle(neighbors)
                nr, nc, cur_wall, nbr_wall = neighbors[0]

                # Open the wall between current cell and chosen neighbor
                setattr(maze[r][c],   cur_wall, True)
                setattr(maze[nr][nc], nbr_wall, True)

                visited[nr][nc] = True
                stack.append((nr, nc))

            # If not perfect, punch extra passages to create loops
            if not self.perfect:
                for r in range(height):
                    for c in range(width):
                        if maze[r][c].is_ftwo:
                            continue
                        if r + 1 < height and not maze[r + 1][c].is_ftwo:
                            if random() < 0.1:
                                maze[r][c].south = True
                                maze[r + 1][c].north = True
                        if c + 1 < width and not maze[r][c + 1].is_ftwo:
                            if random() < 0.1:
                                maze[r][c].east = True
                                maze[r][c + 1].west = True

        carve()
        self.benchmark["generation"] = time() - start_time

        self.gen_maze = maze
        return maze

    def maze_solver(self) -> list[Tuple[int, int]]:
        """
        Solves a maze using the Breadth-First Search (BFS) algorithm.

        This function finds the shortest path from the start position to the
        departure position in a maze represented as a 2D grid of `Cell`.
        It traverses only through open walls and avoids revisiting cells.

        The algorithm works as follows:
            1. Start from the given starting cell.
            2. Explore all reachable neighboring cells level by level (BFS).
            3. Track each visited cell and its predecessor.
            4. Stop when the departure cell is reached.
            5. Reconstruct the path by backtracking from the departure to the
            start.
            6. Mark the path in the maze by setting `is_path = True`.

        Args:
            maze (list[list[Cell]]): A 2D grid representing the maze.
            start (Tuple[int, int]): Coordinates (row, col) of the start.
            departure (Tuple[int, int]): Coordinates (row, col) of the target.

        Returns:
            list[Tuple[int, int]]: The shortest path from start to departure as
            list of coordinates. If no path exists, returns a path containing
            only the departure if it was never reached.

        Notes:
            - Movement is allowed only through open walls
            (where the corresponding direction attribute is True).
            - The function modifies the input maze by marking the solution.
        """
        start_time = time()
        directions = {
            "east":  (0,  1),
            "west":  (0, -1),
            "south": (1,  0),
            "north": (-1, 0),
        }
        start = self.entrance
        departure = self.departure
        maze = self.gen_maze

        visited: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start:
                                                                     None}
        queue = deque([start])

        while queue:
            r, c = queue.popleft()

            if (r, c) == departure:
                break

            for wall, (dr, dc) in directions.items():
                if not getattr(maze[r][c], wall):
                    continue
                nr, nc = r + dr, c + dc
                if (nr, nc) in visited:
                    continue
                if not (0 <= nr < len(maze) and 0 <= nc < len(maze[0])):
                    continue
                visited[(nr, nc)] = (r, c)
                queue.append((nr, nc))

        path = []
        current: Optional[Tuple[int, int]] = departure
        while current is not None:
            path.append(current)
            current = visited.get(current)
        path.reverse()

        dir_map = {
            (-1, 0): "⮝",
            (1, 0): "⮟",
            (0, 1): "⮞",
            (0, -1): "⮜"
        }

        # iterate with index to access "next"
        for i in range(len(path)):
            r, c = path[i]
            maze[r][c].is_path = True

            if i < len(path) - 1:
                nr, nc = path[i + 1]
                dr, dc = nr - r, nc - c
                maze[r][c].next_block = dir_map[(dr, dc)]
            else:
                # last cell (departure)
                maze[r][c].next_block = ""

        self.benchmark["solution"] = time() - start_time

        return path


if __name__ == "__main__":
    # Simple test of the maze generator and solver.
    print("=== MazeGenerator Test ===")
    # 21x21 perfect maze with a fixed seed
    gen = MazeGenerator(height=21, width=21,
                        entrance=(0, 0), departure=(20, 20),
                        seed=42, perfect=True)
    maze = gen.generate_maze()
    for row in maze:
        for cell in row:
            print(cell.to_hex(), end="")
        print()

    print(f"\nMaze generated in {gen.benchmark['generation']:.4f} seconds")
    path = gen.maze_solver()
    print(f"Maze solved in {gen.benchmark['solution']:.4f} seconds")
    print(f"Path length: {len(path)}")
    print("Test completed.")
