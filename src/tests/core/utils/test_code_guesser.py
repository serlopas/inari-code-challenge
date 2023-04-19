import random

from app.core.enums.enums import ColorsEnum
from app.core.utils.code_guesser import evaluate_guess, GuessResult
from app.settings.base import get_settings


class TestCodeGuesser:
    def test_evaluate_guess_correct_code(self):
        code = "".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE))

        guess_result = evaluate_guess(code, code)

        assert isinstance(guess_result, GuessResult)
        assert guess_result.black_pegs == get_settings().CODE_SIZE
        assert guess_result.white_pegs == 0

    def test_evaluate_guess_black_and_white(self):
        guess_result = evaluate_guess("rggb", "bggr")

        assert isinstance(guess_result, GuessResult)
        assert guess_result.black_pegs == 2
        assert guess_result.white_pegs == 2

    def test_evaluate_guess_check_black_white(self):
        guess_result = evaluate_guess("rggb", "gggg")

        assert isinstance(guess_result, GuessResult)
        assert guess_result.black_pegs == 2
        assert guess_result.white_pegs == 0
