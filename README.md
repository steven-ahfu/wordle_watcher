# Wordle Score Logger

A simple Python script to log historical Wordle scores into a CSV file for tracking and future analysis.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/wordle-score-logger.git
   cd wordle-score-logger
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Rename env-example.py to env.py:
   ```sh
   mv env-example.py env.py
   ```

## Usage

### Logging a Wordle Score

```sh
python log_score.py <name> "<wordle_output>" [--date YYYY-MM-DD]
```

- `<name>`: The name of the player
- `<wordle_output>`: The Wordle output (must be quoted)
- `--date YYYY-MM-DD` (optional): The date of the game; defaults to today if not provided

Example:

```sh
python log_score.py Alice """Wordle 1360 5/6*\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩\n\nWordleBot\nSkill 99/99\nLuck 45/99"""
```

### Analyzing the Scores

```sh
python analyze_scores.py

Most unlucky: Joshua, 34.5
Lucky mf: Davon, 32.0
Most skilled: Shlomo, 20.0
Garbage: Junqi, 0.3
```

## Running Tests

To run all tests:

```sh
python -m unittest discover
```

To run a specific test:

```sh
python -m unittest test_log_score.TestLogScore.test_valid_wordle_output
```

## Pre-commit Hook

This project uses `pre-commit` to automatically run tests and linting before commits.

### Setup

1. Install `pre-commit`:
   ```sh
   pip install pre-commit
   ```
2. Install the hooks:
   ```sh
   pre-commit install
   ```

Now, every time you commit, the hooks will run automatically to check for linting issues and run all tests.

To manually run the hooks:

```sh
pre-commit run --all-files
```

## License

This project is licensed under the GNU General Public License v3.0. See `LICENSE` for details.
