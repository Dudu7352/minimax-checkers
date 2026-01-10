
# minimax-checkers

Simple checkers (draughts) game with bot build using minimax algorithm.

## Running the main.py

From the repository root:

```bash
uv sync
uv run python src/main.py
```

## Using the notebooks

You will need to install the dependencies.
From the repository root:

```bash
uv sync
uv sync --dev # installs ipykernel and other nice-to-haves
```

After modifying the source .py files it may be necessary to run `uv sync` / restart the jupyter kernel to use the new code in the notebooks
s
## Notes:

- The project targets Python 3.13+ (see `pyproject.toml` or `.python-version`).
- Dev dependencies for notebooks live under the `dev` dependency group.

## Project Structure

```text
.
├─ pyproject.toml
├─ README.md
├─ notebooks/                        # notebooks used for plots, graphs and research
└─ src/
	├─ main.py                   # entrypoint file for non-library purposes
	└─ checkers/
		├─ minimax.py        # minimax search
		├─ node.py           # game tree node
		├─ state.py          # board/state + move generation/scoring
		└─ print.py          # board printing helpers
```
