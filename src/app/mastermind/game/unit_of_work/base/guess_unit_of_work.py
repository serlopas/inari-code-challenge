from app.core.unit_of_work.unit_of_work import BaseUnitOfWork

from app.mastermind.game.repository.base.guess_repository import GuessRepository


class GuessUnitOfWork(BaseUnitOfWork[GuessRepository]):
    pass
