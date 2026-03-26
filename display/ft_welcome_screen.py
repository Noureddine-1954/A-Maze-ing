from display.menu_print import clear


def print_welcome_screen() -> None:
    """Clear the terminal and display the application title card.
    Blocks until the user presses Enter.
    """
    reset = "\033[0m"
    bold = "\033[1m"

    cyan = "\033[96m"
    magenta = "\033[95m"
    yellow = "\033[93m"
    green = "\033[92m"
    blue = "\033[94m"

    clear()
    print(f"""{cyan}
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║     {bold}{magenta}A - M A Z E - I N G{reset}{cyan}               ║
    ║                                       ║
    ║   {yellow}a maze generator and solver{cyan}         ║
    ║                                       ║
    ║   {green}made by:{cyan}                            ║
    ║     {blue}- nel-mout{cyan}                        ║
    ║     {blue}- ylhamidi{cyan}                        ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
    {reset}""")

    input(f"{bold}{yellow}press enter to begin...{reset} ")
