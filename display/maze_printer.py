from mazegen import Cell
from time import sleep


def print_maze(
    grid: list[list[Cell]],
    color: str = "\033[0m",
    path: bool = False,
    anim: bool = True,
) -> None:
    """Print a maze grid to the terminal with optional color and animation.

    Renders the maze using box-drawing characters, with each cell occupying
    a 3-character wide by 1-character tall area. Walls are drawn using ``+``,
    ``-``, and ``|`` characters. Optionally animates the output by printing
    one character at a time, timed so the full render takes approximately
    3 seconds regardless of maze size.

    Args:
        grid: A 2-D list of ``Cell`` objects representing the maze layout.
            The outer list contains rows and each inner list contains the
            cells within that row.
        color: An ANSI escape code applied as the default foreground color
            throughout the maze. Defaults to the terminal reset code
            ``"\\033[0m"``.
        path: If ``True``, cells marked as part of the solution path are
            highlighted in magenta with a ``·`` character. Defaults to
            ``False``.
        anim: If ``True``, characters are printed one at a time to produce
            a drawing animation. If ``False``, output is written instantly.
            Defaults to ``True``.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Each line is cols*4 + 1 chars wide, there are 2*rows + 1 lines total
    total_chars = (2 * rows + 2) * (cols * 4 + 1)
    chr_time = 3.0 / total_chars if anim else 0

    reset = "\033[0m"

    def cell_char(cell: Cell) -> str:
        """Return the colored display string for a single maze cell.

        Cells are rendered as a 3-character string. Special cell types take
        priority in the following order: start, end, solution path, filled
        (``is_ftwo``), and finally empty.

        Args:
            cell: The ``Cell`` object to render.

        Returns:
            A 3-character string, potentially prefixed and suffixed with ANSI
            escape codes, representing the cell's visual state.
        """
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
