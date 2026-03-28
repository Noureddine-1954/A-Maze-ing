from input_output import (ft_parsing,
                          ConfigError,
                          ft_outputing)
from display import (print_maze,
                     maze_menu,
                     ExitingMaze,
                     clear,
                     print_welcome_screen)
from mazegen import MazeGenerator
from typing import Generator, Tuple


def generate_color() -> Generator[Tuple[str, str], None, None]:
    """Yield maze color names and their ANSI escape codes in a infinite cycle.

    Iterates over a fixed palette of named 256-color ANSI codes and wraps
    around indefinitely, so callers can advance the color on each user
    request without tracking position themselves.

    Yields:
        A ``(name, code)`` tuple where ``name`` is a lowercase color label
        (e.g. ``"green"``) and ``code`` is the corresponding ANSI escape
        string (e.g. ``"\\033[38;5;34m"``).
    """
    all_colors = {
        "green": "\033[38;5;34m",
        "red": "\033[38;5;196m",
        "blue": "\033[38;5;21m",
        "yellow": "\033[38;5;220m",
        "purple": "\033[38;5;129m",
        "white": "\033[0m",
    }

    while True:
        for color in all_colors:
            yield color, all_colors[color]


def main() -> None:
    try:
        config = ft_parsing()
    except ConfigError as e:
        print("Config Error:", e)
        exit(1)

    # this helps as the bridge between the input and the program parameters
    settings = {
        "generate": True,
        "show_path": False,
        "use_seed": True,
        "animation": True
    }
    try:
        print_welcome_screen()
    except BaseException:
        pass

    ht = config["HEIGHT"]
    wd = config["WIDTH"]
    ent = config["ENTRY"]
    ext = config["EXIT"]
    ot_file = config["OUTPUT_FILE"]
    perfect = config["PERFECT"]
    seed = config["SEED"]
    maze_instance = MazeGenerator(ht, wd, ent, ext, seed, perfect)

    gen_colors = generate_color()
    prev = ("white", "\033[0m")

    while True:

        if settings['show_path']:
            showing = "On"
        else:
            showing = "Off"

        coloring = prev[0].capitalize()

        if settings.get('use_seed', False):
            using_seed = seed
        else:
            using_seed = "Off"

        if settings['animation']:
            animating = "On"
        else:
            animating = "Off"

        menu = {
            "1": "Re-generate a new maze",
            "2": f"On/Off show path ({showing})",
            "3": f"Switch maze colors ({coloring})",
            "4": f"On/Off animation ({animating})",
            "5": "Quit",
            "6": f"On/Off seed ({using_seed})",
        }
        if seed is None:
            del menu["6"]

        try:
            clear()
            generate, show_path, use_seed, anim = settings.values()

            if generate:
                maze_instance.seed = seed if use_seed else None
                maze = maze_instance.generate_maze()
                solution = maze_instance.maze_solver()
                ft_outputing(ot_file, maze, ent, ext, solution)
                settings["generate"] = False

            print_maze(maze, prev[1], show_path, anim)

            if wd < 10 or ht < 7:
                print("(The 42 pattern was not printed, too small maze size)")
                print("(min wd: 10, min ht: 7)")

            print("Benchmark: ["
                  f"Generation: {maze_instance.benchmark['generation']:.6f}s |"
                  f" Solution: {maze_instance.benchmark['solution']:.6f}s]",
                  )
            print(len(solution)-1, "steps required to reach the goal!\n")
            choice = maze_menu(menu)
            if choice == "1":
                settings["generate"] = True

            elif choice == "2":
                settings["show_path"] = not settings["show_path"]

            elif choice == "3":
                colors = next(gen_colors)
                prev = colors

            elif choice == "4":
                settings["animation"] = not settings["animation"]

            elif choice == "5":
                raise ExitingMaze("Exiting maze...")

            elif choice == "6":
                settings["use_seed"] = not settings["use_seed"]
                settings["generate"] = True

        except (ExitingMaze, KeyboardInterrupt):
            print("\nExiting maze...")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error of type {type(e).__name__}:", e)
