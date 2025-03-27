import csv
from collections import defaultdict
from env import LOG_FILE
import numpy as np


def parse_score(score_str):
    if score_str == "X":
        return 7
    return int(score_str.split("/")[0])


def calculate_technical_score(skill, attempts, luck):
    return float(float(1 / float(attempts)) * int(skill) * float(1 / float(luck)))


def get_technical_scores(player_stats):
    technical_score_improvement = dict()
    for name, entries in player_stats.items():
        technical_score_improvement[name] = []
        if len(entries["technical_scores"]) > 0:
            # Convert instance keys to integers and sort descending
            sorted_instances = sorted(
                entries["technical_scores"], key=lambda x: x[0], reverse=True
            )
            technical_score_improvement[name] = [list[1] for list in sorted_instances]
    return find_trend(technical_score_improvement)


def find_trend(technical_scores):
    trends = {}
    for name, scores in technical_scores.items():
        scores = np.array(scores)
        x = np.arange(len(scores))
        slope, _ = np.polyfit(x, scores, 1)
        trends[name] = slope

    increasing_most = max(trends, key=trends.get)
    decreasing_most = min(trends, key=trends.get)

    return increasing_most, decreasing_most


def main():
    data = defaultdict(list)
    with open(LOG_FILE, "r") as f:
        # reader = csv.reader(f)
        # next(reader)  # Skip header
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                data[key].append(value)

        # Calculate average luck and skill for each player
        player_stats = defaultdict(
            lambda: {
                "luck": 0,
                "skill": 0,
                "count": 0,
                "technical_score": 0,
                "technical_scores": [],
            }
        )
        for number, name, score, hard_mode, skill, luck in zip(
            data["Wordle Number"],
            data["Name"],
            data["Score"],
            data["Hard Mode"],
            data["Skill"],
            data["Luck"],
        ):
            skill = int(skill)
            luck = int(luck)
            attempts = parse_score(score)
            technical_score = calculate_technical_score(skill, attempts, luck)
            player_stats[name]["luck"] += luck
            player_stats[name]["skill"] += skill
            player_stats[name]["count"] += 1
            player_stats[name]["technical_score"] += technical_score
            player_stats[name]["technical_scores"].append(
                [int(number), technical_score]
            )

        # Calculate average luck and skill for each player
        player_stats = {
            name: {
                "avg_luck": stats["luck"] / stats["count"],
                "avg_skill": stats["skill"] / stats["count"],
                "avg_technical_score": stats["technical_score"] / stats["count"],
                "technical_scores": stats["technical_scores"],
            }
            for name, stats in player_stats.items()
        }

        # Find the player with the lowest average luck
        unlucky_player = min(player_stats, key=lambda x: player_stats[x]["avg_luck"])
        print(
            f"Most unlucky: {unlucky_player}, {player_stats[unlucky_player]['avg_luck']:.1f}"
        )

        # Find the player with the highest average luck
        lucky_player = max(player_stats, key=lambda x: player_stats[x]["avg_luck"])
        print(f"Lucky mf: {lucky_player}, {player_stats[lucky_player]['avg_luck']:.1f}")

        # Find the player with the highest average skill
        most_skilled = max(player_stats, key=lambda x: player_stats[x]["avg_skill"])
        print(
            f"Most skilled: {most_skilled}, {player_stats[most_skilled]['avg_luck']:.1f}"
        )

        # Find the player with the lowest average skill
        garbage = min(
            player_stats, key=lambda x: player_stats[x]["avg_technical_score"]
        )
        print(f"Garbage: {garbage}, {player_stats[garbage]['avg_technical_score']:.1f}")

        # Find the player who appears most in the list
        extremely_online_player = max(data["Name"], key=lambda x: data["Name"].count(x))
        print(f"Extremely online: {extremely_online_player}")

        # Find the player with the highest technical score improvement
        (most_improved_player, least_improved_player) = get_technical_scores(
            player_stats
        )
        print(f"Most improved: {most_improved_player}")

        # Find the player with the lowest technical score improvement
        print(f"Ages like fine piss: {least_improved_player}")


if __name__ == "__main__":
    main()
