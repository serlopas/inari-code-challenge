from app.core.unit_of_work.unit_of_work import BaseUnitOfWork

from app.mastermind.game.domain.repositories.game_repository import GameRepository


class GameUnitOfWork(BaseUnitOfWork[GameRepository]):
    pass
