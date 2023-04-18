import random
import uuid
from abc import abstractmethod
from datetime import datetime

from app.core.enums.enums import ColorsEnum, GameStatusEnum
from app.core.use_cases.use_case import BaseUseCase
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.unit_of_work.game_unit_of_work import GameUnitOfWork
from app.settings.base import get_settings


class CreateGameUseCase(BaseUseCase[None, GameReadModel]):
    unit_of_work: GameUnitOfWork

    @abstractmethod
    def __call__(self, _) -> GameReadModel:
        raise NotImplementedError()


class CreateGameUseCaseImpl(CreateGameUseCase):
    def __init__(self, unit_of_work: GameUnitOfWork):
        self.unit_of_work = unit_of_work

    def __call__(self, _) -> GameReadModel:
        game = GameEntity(
            id=uuid.uuid4().hex,
            code="".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE)),
            tries=0,
            max_tries=get_settings().MAX_TRIES,
            status=GameStatusEnum.in_progress,
            created_at=datetime.now(),
        )

        try:
            created_game: GameEntity = self.unit_of_work.repository.create(game)
        except Exception:
            self.unit_of_work.rollback()
            raise

        self.unit_of_work.commit()

        return GameReadModel.from_entity(created_game)
