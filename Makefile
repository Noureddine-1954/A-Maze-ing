PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

install:
	pip install -r requirements.txt --break-system-packages

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -name "*.pyc" -delete

lint:
	@python3 -m flake8 .
	@python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@python3 -m flake8 .
	@python3 -m mypy . --strict