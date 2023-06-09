from app.mastermind.game.repository.base.guess_repository import GuessRepository
from app.mastermind.game.unit_of_work.base.guess_unit_of_work import GuessUnitOfWork


class GuessUnitOfWorkImpl(GuessUnitOfWork):
    def __init__(self, guess_repository: GuessRepository):
        self.repository: GuessRepository = guess_repository

    def begin(self):
        self.repository.session.begin()

    def commit(self):
        self.repository.session.commit()

    def rollback(self):
        self.repository.session.rollback()
