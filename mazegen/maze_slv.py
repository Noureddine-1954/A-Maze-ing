from collections import deque
from mazegen import Cell
from typing import Optional, Tuple


def maze_solver(maze: list[list[Cell]],
                start: Tuple[int, int],
                departure: Tuple[int, int]) -> list[Tuple[int, int]]:
    """
    Solves a maze using the Breadth-First Search (BFS) algorithm.

    This function finds the shortest path from the start position to the
    departure position in a maze represented as a 2D grid of `Cell` objects.
    It traverses only through open walls and avoids revisiting cells.

    The algorithm works as follows:
        1. Start from the given starting cell.
        2. Explore all reachable neighboring cells level by level (BFS).
        3. Track each visited cell and its predecessor.
        4. Stop when the departure cell is reached.
        5. Reconstruct the path by backtracking from the departure to the
        start.
        6. Mark the path in the maze by setting `is_path = True` on each cell.

    Args:
        maze (list[list[Cell]]): A 2D grid representing the maze.
        start (Tuple[int, int]): Coordinates (row, col) of the starting cell.
        departure (Tuple[int, int]): Coordinates (row, col) of the target cell.

    Returns:
        list[Tuple[int, int]]: The shortest path from start to departure as a
        list of coordinates. If no path exists, returns a path containing only
        the departure if it was never reached.

    Notes:
        - Movement is allowed only through open walls (where the corresponding
          direction attribute is True).
        - The function modifies the input maze by marking the solution path.
    """
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
