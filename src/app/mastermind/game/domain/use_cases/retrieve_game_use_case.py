from abc import abstractmethod
from typing import Tuple

from app.core.error.game_exceptions import GameNotFoundError
from app.core.use_cases.use_case import BaseUseCase
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.services.game_query_service import GameQueryService


class RetrieveGameUseCase(BaseUseCase[Tuple[str], GameReadModel]):
    service: GameQueryService

    @abstractmethod
    def __call__(self, _) -> GameReadModel:
        raise NotImplementedError()


class RetrieveGameUseCaseImpl(RetrieveGameUseCase):
    def __init__(self, service: GameQueryService):
        self.service: GameQueryService = service

    def __call__(self, args: Tuple[str]) -> GameReadModel:
        (id,) = args

        try:
            game = self.service.find_by_id(id)
            if game is None:
                raise GameNotFoundError()
        except Exception:
            raise

        return game
