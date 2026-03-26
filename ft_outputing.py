from mazegen import Cell
from typing import List, Tuple


def ft_outputing(output_file: str,
                 maze: List[List[Cell]],
                 start: Tuple[int, int],
                 departure: Tuple[int, int],
                 solution: List[Tuple[int, int]]
                 ) -> None:
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
