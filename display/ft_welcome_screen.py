from shutil import get_terminal_size
import sys
import time
from display.menu_print import clear


def print_welcome_screen() -> None:
    """Clear the terminal and display the animated application title card.

    Renders a centred box with the app title, subtitle, a decorative maze
    motif, and author credits.  Each line of the box fades in sequentially
    with a short delay, then the prompt is typed out character by character.
    Blocks until the user presses Enter.
    """

    box_width = 36
    rst = "\033[0m"
    bld = "\033[1m"
    dim = "\033[2m"
    blu = "\033[38;5;80m"
    gld = "\033[38;5;220m"
    wht = "\033[97m"
    gry = "\033[38;5;244m"

    terminal_width = get_terminal_size().columns
    pad = max(0, (terminal_width - box_width) // 2) * " "

    lines = [
      f"{blu}{pad+'        '}('ctrl+c' to skip)",
      f"{blu}{pad}┌───────────────────────────────┐",
      f"{blu}{pad}│                               │",
      f"{blu}{pad}│      {bld}{wht}A ─ M A Z E ─ I N G{rst}{blu}      │",
      f"{blu}{pad}│ {dim}{gry}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{rst}{blu} │",
      f"{blu}{pad}│                               │",
      f"{blu}{pad}│   {gry}a maze generator & solver{blu}   │",
      f"{blu}{pad}│                               │",
      f"{blu}{pad}│       {dim}{blu}┌──┐  ╶─┐  ┌──┐{rst}{blu}         │",
      f"{blu}{pad}│       {dim}{blu}│  └──┐ │  │  │{rst}{blu}         │",
      f"{blu}{pad}│       {dim}{blu}└─────┘ └──┘  ╵{rst}{blu}         │",
      f"{blu}{pad}│                               │",
      f"{blu}{pad}│   {gry}by {gld}nel-mout{gry}  &  {gld}ylhamidi{blu}    │",
      f"{blu}{pad}│                               │",
      f"{blu}{pad}└───────────────────────────────┘{rst}",
    ]

    clear()
    print()
    for line in lines:
        time.sleep(0.15)
        print(line)

    # character by character prompt
    prompt = "press enter to begin ›..."
    print()
    sys.stdout.write(f"{pad}  {dim}{gry}")
    for ch in prompt:
        print(bld + gld + ch if ch not in (" ", "›", ".") else gry + ch,
              flush=True, end="")
        time.sleep(0.07)

    input(" ")
