from app.mastermind.game.domain.repositories.game_repository import GameRepository
from app.mastermind.game.domain.unit_of_work.game_unit_of_work import GameUnitOfWork


class GameUnitOfWorkImpl(GameUnitOfWork):
    def __init__(self, game_repository: GameRepository):
        self.repository: GameRepository = game_repository

    def begin(self):
        self.repository.session.begin()

    def commit(self):
        self.repository.session.commit()

    def rollback(self):
        self.repository.session.rollback()
