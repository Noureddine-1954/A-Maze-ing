from ft_parsing import ft_parsing, ConfigError
from mazegen import MazeGenerator, maze_solver
from display import (print_maze,
                     maze_menu,
                     ExitingMaze,
                     clear,
                     print_welcome_screen)
from ft_outputing import ft_outputing
from typing import Generator, Tuple

# program setps
# parsing ...
# generate maze
# print it and the menu
# options etc...


def generate_color() -> Generator[Tuple[str, str], None, None]:
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


if __name__ == "__main__":
    try:
        config = ft_parsing()
    except ConfigError as e:
        print("Config Error:", e)
        exit(1)

    # this helps as the bridge between the input and the program paramters
    settings = {
        "generate": True,
        "show_path": False,
        "use_seed": True,
        "animation": True
    }
    try:
        print_welcome_screen()
    except BaseException:
        print("\nExiting Program...")
        exit(0)

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
    # if seed is None:
    #     del settings["use_seed"]
    # this is for the config file width, height...
    while True:

        # this helps make a dynamic menu
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
            # wether to generate, change colors, show path or not
            generate, show_path, use_seed, anim = settings.values()
            # this is for settings

            # this is always true at the start of the program
            # automatically generate, solve and output in the ot_file
            if generate:
                # init the seed obj if allowed in the settings
                maze_instance.seed = seed if use_seed else None
                # gen the maze
                maze = maze_instance.generate_maze()
                # solve the maze
                solution = maze_solver(maze, ent, ext)
                # output the maze in the file
                ft_outputing(ot_file, maze, ent, ext, solution)
                # after generating the maze
                # we only generate it again after the user chooses 1
                settings["generate"] = False

            # this is where the maze gets printed
            print_maze(maze, prev[1], show_path, anim)

            if wd < 10 or ht < 7:
                print("(The 42 pattern was not printed, too small maze size)")
                print("(min wd: 10, min ht: 7)")

            # the choice from the menu impacts the predefined settings
            choice = maze_menu(menu)
            if choice == "1":  # this is used as the base condition for gen
                settings["generate"] = True

            elif choice == "2":  # this changes the print_maze parameter
                settings["show_path"] = not settings["show_path"]

            elif choice == "3":  # this changes the print_maze parameter
                colors = next(gen_colors)
                prev = colors

            elif choice == "4":  # this just quits the program
                settings["animation"] = not settings["animation"]

            elif choice == "5":  # this just quits the program
                raise ExitingMaze("Exiting maze...")

            elif choice == "6":  # this impacts the maze_generator param
                settings["use_seed"] = not settings["use_seed"]
                settings["generate"] = True

        except (ExitingMaze, KeyboardInterrupt):
            print("\nExiting maze...")
            break
