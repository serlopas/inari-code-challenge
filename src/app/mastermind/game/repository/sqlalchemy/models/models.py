from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.postgres.models import Base
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel


class Game(Base):
    """
    Game DTO is an object associated with game entity
    """

    __tablename__ = "games"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    tries: Mapped[int] = mapped_column(nullable=False)
    max_tries: Mapped[int] = mapped_column(nullable=False)

    guesses: Mapped[list[Guess]] = relationship(back_populates="game")

    def to_entity(self) -> GameEntity:
        return GameEntity(
            id=self.id,
            code=self.code,
            status=self.status,
            tries=self.tries,
            max_tries=self.max_tries,
            guesses=[guess.to_entity() for guess in self.guesses] if self.guesses else [],
            created_at=self.created_at,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "status": self.status,
            "tries": self.tries,
            "max_tries": self.max_tries,
            "guesses": [guess.to_dict() for guess in self.guesses] if self.guesses else [],
            "created_at": self.created_at,
        }

    def to_read_model(self) -> GameReadModel:
        return GameReadModel(
            id=self.id,
            code=self.code,
            status=self.status,
            tries=self.tries,
            max_tries=self.max_tries,
            guesses=[guess.to_read_model() for guess in self.guesses] if self.guesses else [],
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(game: GameEntity):
        return Game(
            id=game.id,
            code=game.code,
            status=game.status,
            tries=game.tries,
            max_tries=game.max_tries,
            guesses=[Guess.from_entity(guess) for guess in game.guesses] if game.guesses else [],
            created_at=game.created_at,
        )


class Guess(Base):
    """
    Guesses DTO is an object associated with guess entity
    """

    __tablename__ = "guesses"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    guess_code: Mapped[str] = mapped_column(nullable=False)
    white_pegs: Mapped[int] = mapped_column(nullable=False)
    black_pegs: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"))

    game: Mapped[Game] = relationship(back_populates="guesses")

    def to_entity(self) -> GuessEntity:
        return GuessEntity(
            id=self.id,
            guess_code=self.guess_code,
            white_pegs=self.white_pegs,
            black_pegs=self.black_pegs,
            game_id=self.game_id,
            created_at=self.created_at,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "guess_code": self.guess_code,
            "white_pegs": self.white_pegs,
            "black_pegs": self.black_pegs,
            "game_id": self.game_id,
            "created_at": self.created_at,
        }

    def to_read_model(self) -> GuessReadModel:
        return GuessReadModel(
            id=self.id,
            guess_code=self.guess_code,
            white_pegs=self.white_pegs,
            black_pegs=self.black_pegs,
            game_id=self.game_id,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(guess: GuessEntity) -> "Guess":
        return Guess(
            id=guess.id,
            guess_code=guess.guess_code,
            white_pegs=guess.white_pegs,
            black_pegs=guess.black_pegs,
            game_id=guess.game_id,
            created_at=guess.created_at,
        )
