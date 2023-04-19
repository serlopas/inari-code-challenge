from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database.postgres.database import get_session
from app.mastermind.game.repository.sqlalchemy.impl.game_repository_impl import SqlAlchemyGameRepositoryImpl
from app.mastermind.game.repository.sqlalchemy.impl.guess_repository_impl import SqlAlchemyGuessRepositoryImpl
from app.mastermind.game.unit_of_work.impl.game_unit_of_work_impl import GameUnitOfWorkImpl
from app.mastermind.game.unit_of_work.impl.game_query_service_impl import GameQueryServiceImpl
from app.mastermind.game.unit_of_work.impl.guess_unit_of_work_impl import GuessUnitOfWorkImpl
from app.mastermind.game.repository.base.game_repository import GameRepository
from app.mastermind.game.repository.base.guess_repository import GuessRepository
from app.mastermind.game.unit_of_work.base.game_query_service import GameQueryService
from app.mastermind.game.unit_of_work.base.game_unit_of_work import GameUnitOfWork
from app.mastermind.game.unit_of_work.base.guess_unit_of_work import GuessUnitOfWork
from app.mastermind.game.unit_of_work.use_cases.create_game_use_case import CreateGameUseCase, CreateGameUseCaseImpl
from app.mastermind.game.unit_of_work.use_cases.create_guess_use_case import CreateGuessUseCaseImpl
from app.mastermind.game.unit_of_work.use_cases.retrieve_game_use_case import (
    RetrieveGameUseCase,
    RetrieveGameUseCaseImpl,
)


def get_game_query_service(session: Session = Depends(get_session)) -> GameQueryService:
    return GameQueryServiceImpl(session)


def get_game_repository(session: Session = Depends(get_session)) -> GameRepository:
    return SqlAlchemyGameRepositoryImpl(session)


def get_guess_repository(session: Session = Depends(get_session)) -> GuessRepository:
    return SqlAlchemyGuessRepositoryImpl(session)


def get_game_unit_of_work(
    game_repository: GameRepository = Depends(get_game_repository),
) -> GameUnitOfWork:
    return GameUnitOfWorkImpl(game_repository)


def get_guess_unit_of_work(
    guess_repository: GuessRepository = Depends(get_guess_repository),
) -> GuessUnitOfWork:
    return GuessUnitOfWorkImpl(guess_repository)


def get_create_game_use_case(unit_of_work: GameUnitOfWork = Depends(get_game_unit_of_work)) -> CreateGameUseCase:
    return CreateGameUseCaseImpl(unit_of_work)


def get_retrieve_game_use_case(service: GameQueryService = Depends(get_game_query_service)) -> RetrieveGameUseCase:
    return RetrieveGameUseCaseImpl(service)


def get_create_guess_use_case(
    game_unit_of_work: GameUnitOfWork = Depends(get_game_unit_of_work),
    guess_unit_of_work: GuessUnitOfWork = Depends(get_guess_unit_of_work),
):
    return CreateGuessUseCaseImpl(game_unit_of_work, guess_unit_of_work)
