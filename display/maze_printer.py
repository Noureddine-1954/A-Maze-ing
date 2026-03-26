from mazegen import Cell
from time import sleep


def print_maze(grid: list[list[Cell]],
               color: str = "\033[0m",
               path: bool = False,
               anim: bool = True) -> None:
    rows = len(grid)
    cols = len(grid[0])

    # Each line is cols*4 + 1 chars wide, there are 2*rows + 1 lines total
    total_chars = (2 * rows + 2) * (cols * 4 + 1)
    chr_time = 3.0 / total_chars if anim else 0

    reset = "\033[0m"

    def cell_char(cell: Cell) -> str:
        if cell.is_start:
            return '\033[32m S ' + color
        if cell.is_end:
            return '\033[31m X ' + color
        if cell.is_path and path:
            return '\033[35m . ' + color
        if cell.is_ftwo:
            return '\033[0m███' + color
        return '   '

    buffer = (color + '+' + '+'.join('---' for _ in range(cols)) + '+' + reset)
    for chr in buffer:
        sleep(chr_time)
        print(chr, end="", flush=True)
    print()

    for r in range(rows):
        row_mid = '|'
        for c in range(cols):
            cell = grid[r][c]
            row_mid += f'{cell_char(cell)}'
            if c == cols - 1:
                row_mid += '|'
            else:
                row_mid += ' ' if cell.east else '|'

        buffer = (color + row_mid + reset)
        for chr in buffer:
            sleep(chr_time)
            print(chr, end="", flush=True)
        print()

        row_bot = '+'
        for c in range(cols):
            cell = grid[r][c]
            row_bot += '   ' if cell.south else '---'
            row_bot += '+'

        if r == rows - 1:
            buffer = (color + "+---" * cols + '+' + reset)
        else:
            buffer = (color + row_bot + reset)

        for chr in buffer:
            sleep(chr_time)
            print(chr, end="", flush=True)
        print()
