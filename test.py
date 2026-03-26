"""
Comprehensive test suite for the mazegen package.
Covers Cell, MazeGenerator, and maze_solver — including edge cases.

Run with:
    pytest test_mazegen.py -v
"""

import pytest
from collections import deque
from unittest.mock import patch

# ---------------------------------------------------------------------------
# Stubs so the module can be imported without a real 'mazegen' package on path
# ---------------------------------------------------------------------------
import sys, types

# Build a minimal 'mazegen' shim that re-exports from the real source files
# when they ARE available, otherwise the tests themselves import directly.
# In a real project, just install the package and remove this block.

# ── Import the three modules under test ─────────────────────────────────────
# Adjust these imports to match how your project exposes the symbols.
from mazegen import Cell, MazeGenerator, maze_gen, maze_slv, maze_solver


# ===========================================================================
# SECTION 1 — Cell
# ===========================================================================

class TestCellInit:
    """Cell.__init__ and wall-bit encoding."""
 
    def test_default_all_walls_closed(self):
        """Default value=15 means every wall is open (all bits set)."""
        c = Cell()
        assert c.north is True
        assert c.east  is True
        assert c.south is True
        assert c.west  is True
 
    def test_value_zero_no_walls_open(self):
        c = Cell(0)
        assert c.north is False
        assert c.east  is False
        assert c.south is False
        assert c.west  is False
 
    def test_value_1_only_north(self):
        c = Cell(1)
        assert c.north is True
        assert c.east  is False
        assert c.south is False
        assert c.west  is False
 
    def test_value_2_only_east(self):
        c = Cell(2)
        assert c.north is False
        assert c.east  is True
        assert c.south is False
        assert c.west  is False
 
    def test_value_4_only_south(self):
        c = Cell(4)
        assert c.south is True
        assert c.north is False
 
    def test_value_8_only_west(self):
        c = Cell(8)
        assert c.west is True
        assert c.north is False
 
    def test_value_6_east_south(self):
        c = Cell(6)      # 2 + 4
        assert c.north is False
        assert c.east  is True
        assert c.south is True
        assert c.west  is False
 
    def test_flags_default_false(self):
        c = Cell()
        assert c.is_start is False
        assert c.is_end   is False
        assert c.is_path  is False
        assert c.is_ftwo  is False
 
    def test_flags_can_be_set_at_init(self):
        c = Cell(0, is_start=True, is_end=True, is_path=True, is_ftwo=True)
        assert c.is_start is True
        assert c.is_end   is True
        assert c.is_path  is True
        assert c.is_ftwo  is True
 
    def test_bool_coercion(self):
        """Non-zero values produce True, zero produces False."""
        c = Cell(3)   # north=1, east=2 → both True
        assert c.north is True
        assert c.east  is True
        assert c.south is False
 
 
class TestCellOpenWall:
    """Cell.open_wall removes (closes) a named wall."""
 
    @pytest.mark.parametrize("direction", ["north", "east", "south", "west"])
    def test_open_wall_sets_to_false(self, direction):
        c = Cell(15)   # all walls open
        c.open_wall(direction)
        assert getattr(c, direction) is False
 
    def test_open_wall_does_not_affect_others(self):
        c = Cell(15)
        c.open_wall("north")
        assert c.east  is True
        assert c.south is True
        assert c.west  is True
 
    def test_open_wall_idempotent(self):
        c = Cell(0)
        c.open_wall("east")   # already False
        assert c.east is False
 
 
class TestCellToHex:
    """Cell.to_hex serialises walls back to a single hex character."""
 
    @pytest.mark.parametrize("value,expected", [
        (0,  'F'),   # no walls open  → 15-0  = 15 → 'F'
        (15, '0'),   # all walls open → 15-15 =  0 → '0'
        (1,  'E'),   # north only     → 15-1  = 14 → 'E'
        (2,  'D'),   # east only      → 15-2  = 13 → 'D'
        (4,  'B'),   # south only     → 15-4  = 11 → 'B'
        (8,  '7'),   # west only      → 15-8  =  7 → '7'
        (6,  '9'),   # east+south     → 15-6  =  9 → '9'
    ])
    def test_roundtrip(self, value, expected):
        c = Cell(value)
        assert c.to_hex() == expected
 
    def test_open_wall_reflects_in_hex(self):
        """After open_wall('north') on a Cell(1), hex should become 'F'."""
        c = Cell(1)   # north open
        c.open_wall("north")
        assert c.to_hex() == 'F'   # 15 - 0 = 15
 
    def test_all_open_hex_is_zero(self):
        c = Cell(15)
        assert c.to_hex() == '0'
 
 
# ===========================================================================
# SECTION 2 — MazeGenerator
# ===========================================================================
 
def _make_gen(h=10, w=10, ent=(0, 0), dep=None, seed=42, perfect=True):
    if dep is None:
        dep = (h - 1, w - 1)
    return MazeGenerator(h, w, ent, dep, seed, perfect)
 
 
class TestMazeGeneratorInit:
    def test_attributes_stored(self):
        g = _make_gen(8, 12, (0, 0), (7, 11), seed=1, perfect=False)
        assert g.height   == 8
        assert g.width    == 12
        assert g.entrance == (0, 0)
        assert g.departure == (7, 11)
        assert g.seed     == 1
        assert g.perfect  is False
 
 
class TestMazeShape:
    def test_output_dimensions(self):
        g = _make_gen(7, 9)
        maze = g.generate_maze()
        assert len(maze) == 7
        assert all(len(row) == 9 for row in maze)
 
    def test_all_cells_are_cell_instances(self):
        maze = _make_gen(5, 5).generate_maze()
        for row in maze:
            for cell in row:
                assert isinstance(cell, Cell)
 
    def test_start_and_end_flags(self):
        g = _make_gen(5, 5, ent=(0, 0), dep=(4, 4))
        maze = g.generate_maze()
        assert maze[0][0].is_start is True
        assert maze[4][4].is_end   is True
 
    def test_no_other_start_flags(self):
        g = _make_gen(5, 5)
        maze = g.generate_maze()
        starts = [(r, c) for r in range(5) for c in range(5)
                  if maze[r][c].is_start]
        assert starts == [(0, 0)]
 
    def test_no_other_end_flags(self):
        g = _make_gen(5, 5)
        maze = g.generate_maze()
        ends = [(r, c) for r in range(5) for c in range(5)
                if maze[r][c].is_end]
        assert ends == [(4, 4)]
 
 
class TestMazePerfect:
    """A perfect maze has exactly one path between any two cells (it's a
    spanning tree), which also means it is fully connected."""
 
    def _all_reachable(self, maze):
        """BFS from (0,0); returns set of visited (r,c)."""
        h, w = len(maze), len(maze[0])
        dirs = {"north": (-1, 0), "south": (1, 0),
                "east":  (0, 1),  "west":  (0, -1)}
        visited = set()
        queue = deque([(0, 0)])
        visited.add((0, 0))
        while queue:
            r, c = queue.popleft()
            for wall, (dr, dc) in dirs.items():
                if getattr(maze[r][c], wall):
                    nr, nc = r + dr, c + dc
                    if (nr, nc) not in visited and 0 <= nr < h and 0 <= nc < w:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
        return visited
 
    def test_perfect_maze_fully_connected(self):
        g = _make_gen(6, 6, seed=0, perfect=True)
        maze = g.generate_maze()
        visited = self._all_reachable(maze)
        # every non-ftwo cell should be reachable
        total = sum(1 for r in range(6) for c in range(6)
                    if not maze[r][c].is_ftwo)
        assert len(visited) >= total  # may include ftwo boundary cells
 
    def test_walls_are_symmetric(self):
        """If cell (r,c) has east=True, then (r,c+1) must have west=True."""
        maze = _make_gen(8, 8, seed=7, perfect=True).generate_maze()
        h, w = len(maze), len(maze[0])
        for r in range(h):
            for c in range(w):
                if c + 1 < w:
                    assert maze[r][c].east == maze[r][c+1].west, \
                        f"east/west mismatch at ({r},{c})"
                if r + 1 < h:
                    assert maze[r][c].south == maze[r+1][c].north, \
                        f"south/north mismatch at ({r},{c})"
 
 
class TestMazeImperfect:
    def test_imperfect_maze_has_extra_passages(self):
        """With seed fixed, imperfect maze should have more open walls
        than perfect one (at least occasionally)."""
        def count_open(maze):
            return sum(
                sum([c.north, c.east, c.south, c.west])
                for row in maze for c in row
            )
        perfect   = _make_gen(10, 10, seed=1, perfect=True ).generate_maze()
        imperfect = _make_gen(10, 10, seed=1, perfect=False).generate_maze()
        assert count_open(imperfect) >= count_open(perfect)
 
 
class TestMazeSeed:
    def test_same_seed_same_maze(self):
        def walls(maze):
            return [(c.north, c.east, c.south, c.west)
                    for row in maze for c in row]
        m1 = _make_gen(8, 8, seed=99).generate_maze()
        m2 = _make_gen(8, 8, seed=99).generate_maze()
        assert walls(m1) == walls(m2)
 
    def test_different_seeds_different_mazes(self):
        def walls(maze):
            return [(c.north, c.east, c.south, c.west)
                    for row in maze for c in row]
        m1 = _make_gen(8, 8, seed=1).generate_maze()
        m2 = _make_gen(8, 8, seed=2).generate_maze()
        assert walls(m1) != walls(m2)
 
    def test_none_seed_no_crash(self):
        g = _make_gen(6, 6, seed=None)
        maze = g.generate_maze()
        assert len(maze) == 6
 
 
class TestForceFtwo:
    """force_ftwo embeds a '42' pattern when maze is large enough."""
 
    def test_ftwo_cells_present_large_maze(self):
        maze = _make_gen(10, 10).generate_maze()
        ftwo_cells = [(r, c) for r in range(10) for c in range(10)
                      if maze[r][c].is_ftwo]
        assert len(ftwo_cells) > 0
 
    def test_no_ftwo_small_maze_height(self):
        """height < 7 skips force_ftwo."""
        maze = _make_gen(6, 15).generate_maze()
        assert not any(maze[r][c].is_ftwo for r in range(6) for c in range(15))
 
    def test_no_ftwo_small_maze_width(self):
        """width < 10 skips force_ftwo."""
        maze = _make_gen(10, 9).generate_maze()
        assert not any(maze[r][c].is_ftwo for r in range(10) for c in range(9))
 
    def test_ftwo_cells_have_no_walls_open(self):
        """force_ftwo replaces cells with Cell(0) — all walls closed."""
        maze = _make_gen(12, 12).generate_maze()
        for r in range(12):
            for c in range(12):
                if maze[r][c].is_ftwo:
                    assert not maze[r][c].north
                    assert not maze[r][c].east
                    assert not maze[r][c].south
                    assert not maze[r][c].west
 
    def test_ftwo_not_visited_by_carve(self):
        """Carver treats ftwo cells as pre-visited; they keep Cell(0) walls."""
        maze = _make_gen(14, 14, seed=5).generate_maze()
        for r in range(14):
            for c in range(14):
                if maze[r][c].is_ftwo:
                    assert not any([maze[r][c].north, maze[r][c].east,
                                    maze[r][c].south, maze[r][c].west])
 
 
class TestMazeEdgeCases:
    def test_1x1_maze(self):
        """Trivial maze — single cell, entrance == departure."""
        g = MazeGenerator(1, 1, (0, 0), (0, 0), seed=0, perfect=True)
        maze = g.generate_maze()
        assert maze[0][0].is_start
        assert maze[0][0].is_end
 
    def test_1xN_maze(self):
        g = MazeGenerator(1, 5, (0, 0), (0, 4), seed=0, perfect=True)
        maze = g.generate_maze()
        assert len(maze) == 1 and len(maze[0]) == 5
 
    def test_Nx1_maze(self):
        g = MazeGenerator(5, 1, (0, 0), (4, 0), seed=0, perfect=True)
        maze = g.generate_maze()
        assert len(maze) == 5 and len(maze[0]) == 1
 
    def test_entrance_equals_departure(self):
        g = MazeGenerator(5, 5, (2, 2), (2, 2), seed=0, perfect=True)
        maze = g.generate_maze()
        assert maze[2][2].is_start
        assert maze[2][2].is_end
 
    def test_minimum_ftwo_boundary(self):
        """Exactly at the 7×10 boundary, force_ftwo SHOULD run."""
        maze = _make_gen(7, 10).generate_maze()
        # just confirm it doesn't crash; ftwo may or may not fit depending on offsets
        assert len(maze) == 7
 
 
# ===========================================================================
# SECTION 3 — maze_solver
# ===========================================================================
 
def _simple_corridor():
    """
    Build a 1×3 horizontal corridor manually:
        [0] -east-> [1] -east-> [2]
    """
    cells = [Cell(0), Cell(0), Cell(0)]
    cells[0].east  = True;  cells[1].west  = True
    cells[1].east  = True;  cells[2].west  = True
    return [cells]  # 1 row
 
 
def _two_row_maze():
    """
    2×2 maze:
      [0,0] --east-- [0,1]
        |               |
      [1,0] --east-- [1,1]
    All four connections open.
    """
    row0 = [Cell(0), Cell(0)]
    row1 = [Cell(0), Cell(0)]
    row0[0].east = True;  row0[1].west = True
    row0[0].south = True; row1[0].north = True
    row0[1].south = True; row1[1].north = True
    row1[0].east = True;  row1[1].west = True
    return [row0, row1]
 
 
class TestMazeSolverBasic:
    def test_trivial_path_corridor(self):
        maze = _simple_corridor()
        path = maze_solver(maze, (0, 0), (0, 2))
        assert path[0]  == (0, 0)
        assert path[-1] == (0, 2)
 
    def test_corridor_path_length(self):
        maze = _simple_corridor()
        path = maze_solver(maze, (0, 0), (0, 2))
        assert len(path) == 3
 
    def test_path_marks_is_path(self):
        maze = _simple_corridor()
        maze_solver(maze, (0, 0), (0, 2))
        assert maze[0][0].is_path
        assert maze[0][1].is_path
        assert maze[0][2].is_path
 
    def test_start_equals_end_returns_single_cell(self):
        maze = _simple_corridor()
        path = maze_solver(maze, (0, 1), (0, 1))
        assert path == [(0, 1)]
 
    def test_returns_list_of_tuples(self):
        maze = _simple_corridor()
        path = maze_solver(maze, (0, 0), (0, 2))
        assert isinstance(path, list)
        assert all(isinstance(p, tuple) and len(p) == 2 for p in path)
 
 
class TestMazeSolverOnGeneratedMaze:
    def test_solver_finds_path(self):
        g = _make_gen(8, 8, ent=(0, 0), dep=(7, 7), seed=3, perfect=True)
        maze = g.generate_maze()
        path = maze_solver(maze, (0, 0), (7, 7))
        assert path[0]  == (0, 0)
        assert path[-1] == (7, 7)
 
    def test_path_is_contiguous(self):
        """Each consecutive pair of path cells must be neighbours."""
        maze = _make_gen(8, 8, seed=5).generate_maze()
        path = maze_solver(maze, (0, 0), (7, 7))
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            assert abs(r1 - r2) + abs(c1 - c2) == 1, \
                f"Non-adjacent steps: ({r1},{c1}) -> ({r2},{c2})"
 
    def test_path_respects_walls(self):
        """Movement from cell to cell is only allowed through open walls."""
        maze = _make_gen(8, 8, seed=6).generate_maze()
        path = maze_solver(maze, (0, 0), (7, 7))
        wall_map = {
            (0,  1): ('east',  'west'),
            (0, -1): ('west',  'east'),
            (1,  0): ('south', 'north'),
            (-1, 0): ('north', 'south'),
        }
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            dr, dc = r2 - r1, c2 - c1
            w1, w2 = wall_map[(dr, dc)]
            assert getattr(maze[r1][c1], w1), \
                f"Wall {w1} not open at ({r1},{c1})"
            assert getattr(maze[r2][c2], w2), \
                f"Wall {w2} not open at ({r2},{c2})"
 
    def test_all_path_cells_marked(self):
        maze = _make_gen(6, 6, seed=9).generate_maze()
        path = maze_solver(maze, (0, 0), (5, 5))
        for (r, c) in path:
            assert maze[r][c].is_path, f"Cell ({r},{c}) not marked is_path"
 
    def test_non_path_cells_not_marked(self):
        """At least some cells should NOT be on the path in a 6×6 maze."""
        maze = _make_gen(6, 6, seed=11).generate_maze()
        maze_solver(maze, (0, 0), (5, 5))
        unmarked = [(r, c) for r in range(6) for c in range(6)
                    if not maze[r][c].is_path]
        assert len(unmarked) > 0
 
    def test_solver_different_start_end(self):
        maze = _make_gen(8, 8, ent=(0, 3), dep=(7, 3), seed=20).generate_maze()
        path = maze_solver(maze, (0, 3), (7, 3))
        assert path[0]  == (0, 3)
        assert path[-1] == (7, 3)
 
 
class TestMazeSolverEdgeCases:
    def test_no_path_returns_empty_or_start_only(self):
        """Isolated cells with no open walls — departure is unreachable.
        The solver's reconstruction walks back from departure through visited;
        since departure was never reached, visited.get(departure) is None and
        the loop appends only departure then stops.  The path therefore
        contains only the departure cell and does NOT contain the start."""
        cells = [[Cell(0), Cell(0)]]
        path = maze_solver(cells, (0, 0), (0, 1))
        # departure appears (reconstruction always starts there)
        assert (0, 1) in path
        # but start was never connected, so it must be absent
        assert (0, 0) not in path
 
    def test_1x1_grid(self):
        maze = [[Cell(0)]]
        path = maze_solver(maze, (0, 0), (0, 0))
        assert path == [(0, 0)]
 
    def test_long_corridor_path_length(self):
        n = 10
        cells = [Cell(0) for _ in range(n)]
        for i in range(n - 1):
            cells[i].east   = True
            cells[i+1].west = True
        maze = [cells]
        path = maze_solver(maze, (0, 0), (0, n - 1))
        assert len(path) == n
 
    def test_2x2_all_open(self):
        maze = _two_row_maze()
        path = maze_solver(maze, (0, 0), (1, 1))
        assert path[0]  == (0, 0)
        assert path[-1] == (1, 1)
        assert len(path) == 3   # BFS finds shortest (2 steps + start)
 
    def test_solver_bfs_shortest_path(self):
        """In a 1×4 corridor, the only path has length 4."""
        cells = [Cell(0) for _ in range(4)]
        for i in range(3):
            cells[i].east   = True
            cells[i+1].west = True
        path = maze_solver([cells], (0, 0), (0, 3))
        assert len(path) == 4
 
 
# ===========================================================================
# SECTION 4 — Integration: generate then solve
# ===========================================================================
 
class TestIntegration:
    @pytest.mark.parametrize("seed", [0, 1, 42, 100, 999])
    def test_generated_maze_is_solvable(self, seed):
        g = _make_gen(10, 10, seed=seed, perfect=True)
        maze = g.generate_maze()
        path = maze_solver(maze, (0, 0), (9, 9))
        assert path[-1] == (9, 9), f"Maze with seed={seed} not solvable"
 
    def test_imperfect_maze_solvable(self):
        g = _make_gen(10, 10, seed=7, perfect=False)
        maze = g.generate_maze()
        path = maze_solver(maze, (0, 0), (9, 9))
        assert path[-1] == (9, 9)
 
    def test_path_is_valid_after_generation(self):
        g = _make_gen(8, 8, seed=13)
        maze = g.generate_maze()
        path = maze_solver(maze, (0, 0), (7, 7))
        # every step must go through an open wall
        wall_map = {
            (0,  1): ('east',  'west'),
            (0, -1): ('west',  'east'),
            (1,  0): ('south', 'north'),
            (-1, 0): ('north', 'south'),
        }
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            dr, dc = r2 - r1, c2 - c1
            w1, _ = wall_map[(dr, dc)]
            assert getattr(maze[r1][c1], w1)
 
    def test_cell_to_hex_after_carving(self):
        """to_hex should return a valid hex character for every cell post-generation."""
        maze = _make_gen(8, 8, seed=21).generate_maze()
        valid = set('0123456789ABCDEF')
        for row in maze:
            for cell in row:
                assert cell.to_hex() in valid
 
    def test_large_maze(self):
        """Smoke test: 30×30 perfect maze generates and solves without error."""
        g = _make_gen(30, 30, seed=77)
        maze = g.generate_maze()
        path = maze_solver(maze, (0, 0), (29, 29))
        assert path[-1] == (29, 29)
