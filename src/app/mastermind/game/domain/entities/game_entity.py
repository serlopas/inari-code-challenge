from __future__ import annotations

import typing
from datetime import datetime

from app.mastermind.game.domain.entities.guess_entity import GuessEntity


class GameEntity:
    def __init__(
        self,
        id: str,
        code: str,
        status: str,
        tries: int,
        max_tries: int,
        created_at: typing.Optional[datetime] = None,
        guesses: typing.Optional[list[GuessEntity]] = None,
    ):
        self.id = id
        self.code = code
        self.status = status
        self.tries = tries
        self.max_tries = max_tries
        self.created_at = created_at if created_at else datetime.now()
        self.guesses = guesses

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GameEntity):
            return self.id == other.id

        return False
