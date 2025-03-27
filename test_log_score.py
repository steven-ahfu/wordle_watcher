# To run all tests:
# python -m unittest test_log_score.py
#
# To run a specific test:
# python -m unittest test_log_score.TestLogScore.test_valid_wordle_output

import unittest
from log_score import parse_wordle_output, log_score


class TestLogScore(unittest.TestCase):
    def test_valid_wordle_output(self):
        wordle_output = "Wordle 1360 5/6*\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩\n\nWordleBot\nSkill 99/99\nLuck 45/99"  # noqa: E501
        wordle_number, score, hard_mode, skill, luck = parse_wordle_output(
            wordle_output
        )
        self.assertEqual(wordle_number, "1360")
        self.assertEqual(score, "5")
        self.assertTrue(hard_mode)
        self.assertEqual(skill, 99)
        self.assertEqual(luck, 45)

    def test_invalid_wordle_output(self):
        wordle_output = "Invalid Wordle text"
        with self.assertRaises(ValueError):
            parse_wordle_output(wordle_output)

    def test_hard_mode_parsing(self):
        wordle_output = (
            "Wordle 1000 4/6*\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩"
        )
        _, _, hard_mode, _, _ = parse_wordle_output(wordle_output)
        self.assertTrue(hard_mode)

        wordle_output_no_hard = "Wordle 1001 3/6\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩"
        _, _, hard_mode, _, _ = parse_wordle_output(wordle_output_no_hard)
        self.assertFalse(hard_mode)

    def test_log_score_with_date(self):
        wordle_output = "Wordle 1500 6/6\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩"
        log_score("Alice", wordle_output, "2025-03-10")

    def test_log_score_without_date(self):
        wordle_output = (
            "Wordle 1501 4/6\n\n🟩⬛⬛⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩⬛🟩\n🟩🟩🟩🟩🟩"
        )
        log_score("Bob", wordle_output)  # Should default to today's date


if __name__ == "__main__":
    unittest.main()
