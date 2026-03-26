from ft_parsing import ft_parsing, ConfigError
from mazegen import MazeGenerator, maze_solver
from display import print_maze, maze_menu, ExitingMaze, clear
from ft_outputing import ft_outputing

# program setps
# parsing ...
# generate maze
# print it and the menu
# options etc...

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
        "colors": False,
        "use_seed": True,
        "animation": True
    }

    print(config.values())
    ht = config["HEIGHT"]
    wd = config["WIDTH"]
    ent = config["ENTRY"]
    ext = config["EXIT"]
    ot_file = config["OUTPUT_FILE"]
    perfect = config["PERFECT"]
    seed = config["SEED"]
    maze_instance = MazeGenerator(ht, wd, ent, ext, seed, perfect)
    # this is for the config file width, height...
    while True:

        # this helps make a dynamic menu
        menu = {
            "1": "Re-generate a new maze",
            "2": f"On/Off show path ({settings['show_path']})",
            "3": f"Switch maze colors ({settings['colors']})",
            "4": f"On/Off seed ({settings['use_seed']})",
            "5": f"On/Off animation ({settings['animation']})",
            "6": "Quit"
        }

        try:
            clear()
            # wether to generate, change colors, show path or not
            generate, show_path, colors, use_seed, anim = settings.values()
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
            print_maze(maze, colors, show_path, anim)

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
                settings["colors"] = not settings["colors"]

            elif choice == "4":  # this impacts the maze_generator param
                settings["use_seed"] = not settings["use_seed"]
                settings["generate"] = True

            elif choice == "5":  # this just quits the program
                settings["animation"] = not settings["animation"]

            elif choice == "6":  # this just quits the program
                raise ExitingMaze("Exiting maze...")

        except (ExitingMaze, KeyboardInterrupt):
            print("\nExiting maze...")
            break
