from collections import deque
from mazegen import Cell
from typing import Optional, Tuple


def maze_solver(maze: list[list[Cell]],
                start: Tuple[int, int],
                departure: Tuple[int, int]) -> list[Tuple[int, int]]:
    directions = {
        "east":  (0,  1),
        "west":  (0, -1),
        "south": (1,  0),
        "north": (-1, 0),
    }

    visited: dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
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

    for r, c in path:
        maze[r][c].is_path = True

    return path
