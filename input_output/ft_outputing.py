from mazegen import Cell
from typing import List, Tuple


def ft_outputing(output_file: str,
                 maze: List[List[Cell]],
                 start: Tuple[int, int],
                 departure: Tuple[int, int],
                 solution: List[Tuple[int, int]]
                 ) -> None:
    """Serialise a solved maze to a plain-text output file.

    The file is structured in three sections separated by blank lines:

    1. **Grid** — one line per maze row; each cell is written as its
       hexadecimal wall bitmask via :meth:`Cell.to_hex`.
    2. **Endpoints** — the start and departure coordinates, each on its own
       line in ``row, col`` format (tuple brackets stripped).
    3. **Solution path** — a compact string of cardinal direction characters
       (``N``, ``S``, ``E``, ``W``) encoding each step from ``solution[0]``
       to ``solution[-1]``, with no separators or trailing newline.

    Args:
        output_file: Path to the file to create or overwrite.
        maze: A 2-D list of :class:`Cell` objects representing the full maze
            grid, with the outer list indexing rows and the inner list
            indexing columns.
        start: ``(row, col)`` coordinate of the maze entry point.
        departure: ``(row, col)`` coordinate of the maze exit point.
        solution: Ordered list of ``(row, col)`` coordinates forming the
            solution path from entry to exit, inclusive of both endpoints.

    Raises:
        OSError: If ``output_file`` cannot be opened for writing.
        KeyError: If consecutive solution coordinates produce a step vector
            that is not a unit cardinal move (i.e. the path is not
            contiguous).
    """
    with open(output_file, 'w') as ot_file:
        for row in maze:
            for c in row:
                ot_file.write(c.to_hex())
            ot_file.write('\n')
        ot_file.write('\n')

        ot_file.write(str(start)[1:-1])
        ot_file.write('\n')
        ot_file.write(str(departure)[1:-1])
        ot_file.write('\n')

        directions = {
            (-1, 0): "N",
            (1, 0): "S",
            (0,  1): "E",
            (0, -1): "W"
        }

        last = solution[0]
        for path in solution[1:]:
            step = (path[0] - last[0], path[1] - last[1])
            last = path
            ot_file.write(directions[step])
