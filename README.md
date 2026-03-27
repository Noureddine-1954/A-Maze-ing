*This project has been created as part of the 42 curriculum by nel-mout, ylhamidi.*

#  A-Maze-ing

##  Description

This project consists of generating and solving mazes using algorithmic techniques. The goal is to create a fully functional maze system that can:

* Generate a maze based on configurable parameters
* Solve the maze using a pathfinding algorithm
* Output the result in a structured format

The project emphasizes algorithm design, data structures, and clean code architecture. It also focuses on transforming recursive logic into efficient iterative solutions.

---

##  Instructions

###  Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-name>
```

Make sure you have Python installed (3.10+ recommended).

---

###  Execution

Run your main script (example):

```bash
python main.py config.txt
```

---

###  Running Tests

Install pytest if needed:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

---

##  Config File Structure

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

* `HEIGHT`, `WIDTH`: Dimensions of the maze
* `ENTRY`: Starting position (row, col)
* `EXIT`: Ending position (row, col)
* `PERFECT`: If `True`, generates a perfect maze (no loops)
* `SEED`: Controls randomness for reproducibility
* `OUTPUT_FILE`: File where the maze is saved

---

##  Maze Generation Algorithm

We used an **iterative Depth-First Search (DFS)** algorithm (also known as backtracking).

### How it works:

* Start from the entry point
* Randomly explore neighbors
* Carve paths by removing walls
* Backtrack when no unvisited neighbors remain

---

##  Why This Algorithm?

We chose iterative DFS because:

* It guarantees full maze connectivity
* It is efficient and relatively simple to implement
* It avoids recursion limits (important for large mazes)
* It gives good control over randomness and structure

---

##  Reusable Components

The following parts of the project are reusable:

###  `Cell` class

* Represents each maze cell
* Encodes walls and state (start, end, path, etc.)
* Can be reused in any grid-based system

###  `MazeGenerator` class

* Fully configurable maze generator
* Supports deterministic generation via seed
* Can be reused in games, simulations, or pathfinding systems

###  Solver

* Breadth-First Search (BFS) based
* Works on any compatible grid structure

 Everything outside `if __name__ == "__main__"` is designed to be reusable.

---

##  Team & Project Management

### Roles

* **nel-mout** → Maze generation (DFS, structure, ftwo pattern)
* **ylhamidi** → Maze solving (BFS, pathfinding)

---

###  Planning & Evolution

Initial plan:

* Implement recursive DFS
* Basic grid structure

What changed:

* Switched to **iterative DFS** for better control and performance
* Introduced a **Cell class** to simplify state handling
* Improved modularity and separation of concerns

---

###  What Worked Well

* Clear separation between generation and solving
* Use of classes improved maintainability
* Deterministic generation using seeds
* Testing with pytest helped catch bugs early

---

###  What Could Be Improved

* 

---

##  Tools Used

###  AI

Used for:

* Generating test cases
* Debugging logic issues
* Improving code structure
* Explaining complex concepts (DFS, BFS, etc.)

---

###  pytest

Used for:

* Writing automated tests
* Verifying correctness
* Detecting edge case failures
* Ensuring stability during refactoring

---

##  Resources

* Depth-First Search (DFS) – algorithm references
* Breadth-First Search (BFS) – pathfinding techniques
* Maze generation techniques (recursive backtracking)
* Python documentation
* pytest documentation

---

##  Conclusion

This project provided hands-on experience with:

* Algorithm design
* Iterative vs recursive thinking
* Testing and debugging
* Clean and reusable code architecture

It also highlighted the importance of planning, collaboration, and iteration in software development.
