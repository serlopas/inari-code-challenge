from __future__ import annotations

import typing

from app.mastermind.game.unit_of_work.use_cases.create_game_use_case import CreateGameUseCase
from app.mastermind.game.unit_of_work.use_cases.create_guess_use_case import CreateGuessUseCase, CreateGuessUseCaseArgs
from app.mastermind.game.unit_of_work.use_cases.retrieve_game_use_case import RetrieveGameUseCase, RetrieveGameUseArgs

if typing.TYPE_CHECKING:
    from app.mastermind.game.domain.entities.game_query_model import GameReadModel
    from app.mastermind.game.domain.entities.guess_query_model import GuessGameStatusReadModel


class GameService:
    @classmethod
    def create_game(cls, create_game_use_case: CreateGameUseCase) -> GameReadModel:
        return create_game_use_case(None)

    @classmethod
    def retrieve_game(cls, game_id: str, retrieve_game_use_case: RetrieveGameUseCase) -> GameReadModel:
        return retrieve_game_use_case(RetrieveGameUseArgs(game_id=game_id))

    @classmethod
    def create_guess(
        cls, game_id: str, guess_code: str, create_guess_use_case: CreateGuessUseCase
    ) -> GuessGameStatusReadModel:
        return create_guess_use_case(args=CreateGuessUseCaseArgs(game_id=game_id, guess_code=guess_code))
