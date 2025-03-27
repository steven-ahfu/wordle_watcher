import csv
import re
import argparse
from datetime import datetime
from env import LOG_FILE, NAME_MAP


def get_wordle_number(score_line):
    # Use a regular expression to capture the part of the string that is preceded by a space and succeeded by a space
    match = re.search(r"\s(\d+,\d+)\s", score_line)
    string_score = match.group(1)
    # Replace the comma with an empty string
    string_score_without_comma = string_score.replace(",", "")
    # Convert to int
    return int(string_score_without_comma)


def map_emojis_to_chars(grid):
    # Mapping of emojis to their corresponding characters
    emoji_to_char = {
        "<0001f7e8>": "Y",  # Yellow square
        "🟨": "Y",  # Also yellow square
        "<00002B1B>": "B",  # Black square
        "⬛": "B",  # Black square
        "<00002B1C>": "W",  # Black square
        "⬜": "W",  # Black square
        "<0001f7e9>": "G",  # Green square
        "🟩": "G",  # Green square
    }
    mapped_grid = []
    for row in grid:
        new_row = ""
        for char in row:
            if char in emoji_to_char:
                new_row += emoji_to_char[char]
            else:
                new_row += (
                    char  # Keep the character as is if it's not in the dictionary
                )
        mapped_grid.append(new_row)
    return mapped_grid


def map_name(name):
    sanitze_name = name.lower().strip()

    if sanitze_name in emoji_to_char:
        return NAME_MAP.get(sanitze_name).capitalize()
    else:
        return sanitze_name.capitalize()


def parse_wordle_output(wordle_output):
    """Extracts relevant details from the Wordle output."""
    # Split the grid into lines and then into individual characters
    lines = wordle_output.strip().split("\n")
    score_line = lines.pop(0)
    luck_line = lines.pop(-1)
    skill_link = lines.pop(-1)
    # remove empty lines
    lines.pop(0)
    lines.pop(-1)
    # Whats remaining is the score grid
    # Map to chars
    grid = map_emojis_to_chars(lines)

    # Regex
    score_match = re.search(r"(\d+)/(\d+)", score_line)
    skill_match = re.search(r"Skill (\d+)/99", skill_link)
    luck_match = re.search(r"Luck (\d+)/99", luck_line)

    wordle_number = get_wordle_number(score_line)
    hard_mode = "*" in score_line
    score = score_match.group(1) + "/" + score_match.group(2) if score_match else "X"
    skill = int(skill_match.group(1)) if skill_match else 0
    luck = int(luck_match.group(1)) if luck_match else 0

    return wordle_number, score, hard_mode, skill, luck, "\n".join(grid)


def log_score(name, wordle_output, datestr=None):
    """Logs the Wordle score to a CSV file."""
    # date = datestr if datestr is not None else datetime.today().strftime("%Y-%m-%d")
    wordle_number, score, hard_mode, skill, luck, grid = parse_wordle_output(
        wordle_output
    )

    # Check if the file exists, write headers if not
    write_header = False
    try:
        with open(LOG_FILE, "r", newline="", encoding="utf-8") as file:
            if not file.read():
                write_header = True
    except FileNotFoundError:
        write_header = True

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(
                ["Wordle Number", "Name", "Score", "Hard Mode", "Skill", "Luck", "Grid"]
            )
        writer.writerow(
            [wordle_number, map_name(name), score, hard_mode, skill, luck, grid]
        )

    print("Score logged successfully.")


def main():
    parser = argparse.ArgumentParser(description="Log Wordle scores.")
    parser.add_argument("name", help="Player's name")
    parser.add_argument(
        "wordle_output", help="Raw Wordle output including score and details"
    )
    parser.add_argument(
        "--date",
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date in YYYY-MM-DD format (default: today)",
    )

    args = parser.parse_args()
    log_score(args.name, args.wordle_output, args.date)


if __name__ == "__main__":
    main()
