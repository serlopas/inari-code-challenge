import dataclasses
from collections import defaultdict


@dataclasses.dataclass
class GuessResult:
    black_pegs: int
    white_pegs: int


def evaluate_guess(code: str, guess_code: str) -> GuessResult:
    black_pegs = 0
    white_pegs = 0
    code_digits_count = defaultdict(int)
    guess_digits_count = defaultdict(int)

    for i in range(len(code)):
        if code[i] == guess_code[i]:
            black_pegs += 1
        else:
            code_digits_count[code[i]] = 1
            guess_digits_count[guess_code[i]] = 1

    for digit in guess_digits_count:
        if digit in code_digits_count:
            white_pegs += min(code_digits_count[digit], guess_digits_count[digit])

    return GuessResult(
        black_pegs=black_pegs,
        white_pegs=white_pegs,
    )
