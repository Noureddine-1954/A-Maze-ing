from typing import Optional, Dict


class ExitingMaze(BaseException):
    pass


def clear() -> None:
    print("\033c", end="")


def maze_menu(menu: Dict[str, str]) -> Optional[str]:
    print("=== A-Maze-ing ===")

    def print_menu(menu: Dict[str, str]) -> None:
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
