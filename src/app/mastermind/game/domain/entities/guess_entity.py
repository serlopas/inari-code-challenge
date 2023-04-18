from datetime import datetime
from typing import Optional


class GuessEntity:
    def __init__(
        self,
        id: str,
        guess_code: str,
        white_pegs: int,
        black_pegs: int,
        game_id: str,
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.guess_code = guess_code
        self.white_pegs = white_pegs
        self.black_pegs = black_pegs
        self.game_id = game_id
        self.created_at = created_at

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GuessEntity):
            return self.id == other.id

        return False
