import dataclasses
from abc import abstractmethod

from app.core.error.game_exceptions import GameNotFoundError
from app.core.use_cases.use_case import BaseUseCase
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.unit_of_work.base.game_query_service import GameQueryService


@dataclasses.dataclass
class RetrieveGameUseArgs:
    game_id: str


class RetrieveGameUseCase(BaseUseCase[RetrieveGameUseArgs, GameReadModel]):
    service: GameQueryService

    @abstractmethod
    def __call__(self, args: RetrieveGameUseArgs) -> GameReadModel:
        raise NotImplementedError()


class RetrieveGameUseCaseImpl(RetrieveGameUseCase):
    def __init__(self, service: GameQueryService):
        self.service: GameQueryService = service

    def __call__(self, args: RetrieveGameUseArgs) -> GameReadModel:
        try:
            game = self.service.find_by_id(args.game_id)
            if game is None:
                raise GameNotFoundError()
        except Exception:
            raise

        return game
