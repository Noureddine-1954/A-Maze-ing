from typing import Optional, Tuple
from mazegen import Cell


class MazeGenerator:
    """this is a maze class"""
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

    def generate_maze(self) -> list[list[Cell]]:
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
                            if random() < 0.15:
                                maze[r][c].south = True
                                maze[r + 1][c].north = True
                        if c + 1 < width and not maze[r][c + 1].is_ftwo:
                            if random() < 0.15:
                                maze[r][c].east = True
                                maze[r][c + 1].west = True

        carve()
        return maze
