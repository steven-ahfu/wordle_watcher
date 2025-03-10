import csv
import re
import argparse
from datetime import datetime

LOG_FILE = "wordle_scores.csv"


def parse_wordle_output(wordle_output):
    """Extracts relevant details from the Wordle output."""
    match = re.search(r"Wordle (\d+),? (\d)/6(\*)?", wordle_output)
    if not match:
        raise ValueError("Invalid Wordle output format.")

    wordle_number = match.group(1)
    score = match.group(2)
    hard_mode = bool(match.group(3))

    skill_match = re.search(r"Skill (\d+)/99", wordle_output)
    luck_match = re.search(r"Luck (\d+)/99", wordle_output)

    skill = int(skill_match.group(1)) if skill_match else None
    luck = int(luck_match.group(1)) if luck_match else None

    return wordle_number, score, hard_mode, skill, luck


def log_score(name, wordle_output, datestr=None):
    """Logs the Wordle score to a CSV file."""
    date = datestr if datestr is not None else datetime.today().strftime("%Y-%m-%d")
    wordle_number, score, hard_mode, skill, luck = parse_wordle_output(wordle_output)

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
                ["Date", "Name", "Wordle Number", "Score", "Hard Mode", "Skill", "Luck"]
            )
        writer.writerow([date, name, wordle_number, score, hard_mode, skill, luck])

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
