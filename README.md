*This project has been created as part of the 42 curriculum by nel-mout, ylhamidi.*

# A-Maze-ing

## Description

This project consists of generating and solving mazes using algorithmic techniques. The goal is to create a fully functional maze system that can:

* Generate a maze based on configurable parameters
* Solve the maze using a pathfinding algorithm
* Output the result in a structured format

---

## Instructions

### Installation

Clone the repository:

```bash
git clone git@vogsphere-v2.1337.ma:vogsphere/chintra-uuid-544a240e-34b3-4091-aeba-65f0dc5b7c46-7269955-nel-mout amazing
cd amazing
```

---

### Execution

```bash
make run
```

## Config File Structure

The maze is generated using a configuration file with the following format:

```text
# MazeConfig
HEIGHT = 20
WIDTH = 20
ENTRY = 0, 0
EXIT = 0, 2
PERFECT = False
SEED = 42
OUTPUT_FILE = output_maze.txt
```

### Fields:

* `HEIGHT` ; Height of the maze.
* `WIDTH`: Width of the maze.
* `ENTRY`: Starting position (row, col).
* `EXIT`: Ending position (row, col).
* `PERFECT`: If `True`, generates a perfect maze (no loops).
* `SEED`: Controls randomness for reproducibility (not mandatory).
* `OUTPUT_FILE`: File where the maze is saved.

---

## Maze Generation Algorithm

We used an **iterative Depth-First Search (DFS)** algorithm (also known as backtracking).

### How it works:

* Start from the entry point
* Randomly explore neighbors
* Carve paths by removing walls
* Backtrack when no unvisited neighbors remain

---

## Why This Algorithm?

We chose iterative DFS because:

* It guarantees full maze connectivity
* It is efficient and relatively simple to implement
* It avoids recursion limits (important for large mazes)
* It gives good control over randomness and structure

---

## Reusable Components

The following parts of the project are reusable:

### `Cell` class

* Represents each maze cell
* Encodes walls and state (start, end, path, etc.)
* Can be reused in any grid-based system

### `MazeGenerator` class

* Fully configurable maze generator
* Supports deterministic generation via seed
* Can be reused in games, simulations, or pathfinding systems

### Solver

* Breadth-First Search (BFS)
* Works on any compatible grid structure

Everything outside `if __name__ == "__main__"` is designed to be reusable.

---

## Team & Project Management

### Roles

* **nel-mout** → Maze generation(DFS), Config file parsing, Cell class definition, the main program, the welcome screen and the menu printer.
* **ylhamidi** → Maze solving (BFS), Outputting into the output file and the maze printer.

---

### Planning & Evolution

Initial plan:

* Implement recursive DFS
* Basic grid structure

What changed:

* Switched to **iterative DFS** for better control and performance
* Introduced a **Cell class** to simplify state handling
* Improved modularity and separation of concerns

---

### What Worked Well

* Clear separation between generation and solving
* Use of classes improved maintainability
* Deterministic generation using seeds

---

### What Could Be Improved

* **Maze visualization enhancements**
  Improving the visual output (graphical interface) would make the maze more engaging.

* **Interactive mode**
  Adding a mode where users can step through the maze generation or solving process would improve understanding and usability.

* **Multiple maze generation algorithms**
  Supporting other algorithms (Prim’s, Kruskal’s, etc.) would allow generating different maze styles and structures.

* **Export formats**
  Adding support for exporting mazes in formats like JSON or images could make the project easier to integrate with other systems.

---

## Tools Used

### AI

Used for:

* Generating test cases
* Debugging logic issues
* Improving code structure
* Help with docstrings for code clarity and reusability
* Explaining complex concepts (DFS, BFS, etc.)

## Resources

* Depth-First Search (DFS) – algorithm references [DFS GfG](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/)
* Breadth-First Search (BFS) – pathfinding techniques [BFS GFG](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)
* Python documentation (PEP 257) [Python Docstrings
](https://www.geeksforgeeks.org/python/python-docstrings/)

---

## Conclusion

This project provided hands-on experience with:

* Algorithm design
* Iterative vs recursive thinking
* Testing and debugging
* Clean and reusable code architecture

It also highlighted the importance of planning, collaboration, and iteration in software development.


## Maze Generator Module Section

This module provides the `MazeGenerator` class for generating 2D mazes using a
randomized depth-first search (DFS) algorithm. It supports both perfect mazes
(no cycles) and imperfect mazes (with loops), and can optionally embed a
predefined "42" pattern in the centre. The module also includes a BFS-based
solver to find the shortest path from entrance to exit.

Example:
    
    >>> from mazegen import MazeGenerator

    >>> # Create a 20x20 perfect maze with a fixed seed
    >>> gen = MazeGenerator(height=20, width=20,
    ...                      entrance=(0,0), departure=(19,19),
    ...                      seed=42, perfect=True)
    >>> maze = gen.generate_maze()

    >>> # Solve the maze
    >>> path = gen.maze_solver()

    >>> # Access the grid
    >>> cell = maze[5][5]
    >>> print(cell.east)
    >>> print(cell.east)
  
Run maze_gen directly to see a test of the module