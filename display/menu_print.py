from typing import Optional, Dict
import os


class ExitingMaze(BaseException):
    """Exception raised to signal an intentional exit from the maze.

    Inherits from ``BaseException`` rather than ``Exception`` so that it
    propagates through broad ``except Exception`` handlers, ensuring the
    exit intent is never silently swallowed.
    """

    pass


def clear() -> None:
    """Clear the terminal screen using the shell ``clear`` command."""
    os.system('clear')


def maze_menu(menu: Dict[str, str]) -> Optional[str]:
    """Display the main menu and return the user's validated choice.

    Prints the application title followed by the numbered menu options, then
    blocks until the user enters a key that matches one of the provided
    choices. If any interrupt or exception occurs during input (e.g.
    ``KeyboardInterrupt``, ``EOFError``), the raw exception is caught and
    re-raised as an :class:`ExitingMaze` to allow callers to handle shutdown
    uniformly.

    Args:
        menu: An ordered mapping of choice keys (e.g. ``"1"``, ``"2"``) to
            their human-readable labels (e.g. ``"Start"`, ``"Quit"``). Keys
            are used both for display and for validating user input.

    Returns:
        The key from ``menu`` that the user selected, or ``None`` if the
        input loop has not yet completed (in practice the loop always
        resolves before returning).

    Raises:
        ExitingMaze: If any ``BaseException`` is raised while reading input,
            wrapping it with a user-facing exit message.
    """

    print("=== A-Maze-ing ===")

    def print_menu(menu: Dict[str, str]) -> None:
        """Print each menu entry as ``"<key>. <label>"``.

        Args:
            menu: The same ordered mapping passed to the enclosing
                :func:`maze_menu` call.
        """
        for choice in menu:
            print(choice + ". " + menu[choice])

    try:
        print_menu(menu)
        choice = None
        while choice not in menu:
            choice = input(f"\nChoice? (1-{len(menu)}): ")

        return choice

    except BaseException:
        raise ExitingMaze("\nExiting maze...")
