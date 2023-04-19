import dataclasses
import uuid
from abc import abstractmethod
from datetime import datetime
from typing import Optional

from app.core.enums.enums import GameStatusEnum, ColorsEnum
from app.core.error.game_exceptions import GameNotFoundError, GameAlreadyFinishedError
from app.core.error.guess_exceptions import GuessSizeNotValid, GuessCombinationNotValid
from app.core.use_cases.use_case import BaseUseCase
from app.core.utils import code_guesser
from app.mastermind.game.domain.entities.game_entity import GameEntity
from app.mastermind.game.domain.entities.guess_entity import GuessEntity
from app.mastermind.game.domain.entities.guess_query_model import GuessGameStatusReadModel
from app.mastermind.game.unit_of_work.base.game_unit_of_work import GameUnitOfWork
from app.mastermind.game.unit_of_work.base.guess_unit_of_work import GuessUnitOfWork


@dataclasses.dataclass
class CreateGuessUseCaseArgs:
    game_id: str
    guess_code: str


class CreateGuessUseCase(BaseUseCase[CreateGuessUseCaseArgs, GuessGameStatusReadModel]):
    game_unit_of_work: GameUnitOfWork
    guess_unit_of_work: GuessUnitOfWork

    @abstractmethod
    def __call__(self, args: CreateGuessUseCaseArgs) -> GuessGameStatusReadModel:
        raise NotImplementedError()


class CreateGuessUseCaseImpl(CreateGuessUseCase):
    def __init__(
        self,
        game_unit_of_work: GameUnitOfWork,
        guess_unit_of_work: GuessUnitOfWork,
    ):
        self.game_unit_of_work = game_unit_of_work
        self.guess_unit_of_work = guess_unit_of_work

    def __call__(self, args: CreateGuessUseCaseArgs) -> GuessGameStatusReadModel:
        guess_code = args.guess_code.lower()

        try:
            game: Optional[GameEntity] = self.game_unit_of_work.repository.find_by_id(args.game_id)
            if game is None:
                raise GameNotFoundError()
        except Exception:
            raise

        if game.status in (GameStatusEnum.won, GameStatusEnum.lost):
            raise GameAlreadyFinishedError()

        if len(guess_code) != len(game.code):
            raise GuessSizeNotValid()

        if not all(color in list(ColorsEnum) for color in guess_code):
            raise GuessCombinationNotValid()

        guess_result: code_guesser.GuessResult = code_guesser.evaluate_guess(
            code=game.code,
            guess_code=guess_code,
        )

        guess = GuessEntity(
            id=uuid.uuid4().hex,
            guess_code=guess_code,
            white_pegs=guess_result.white_pegs,
            black_pegs=guess_result.black_pegs,
            game_id=args.game_id,
            created_at=datetime.now(),
        )

        game.tries += 1
        if guess.black_pegs == len(guess_code):
            game.status = GameStatusEnum.won
        elif game.tries == game.max_tries:
            game.status = GameStatusEnum.lost

        try:
            self.guess_unit_of_work.repository.create(guess)
            self.game_unit_of_work.repository.update(game)
        except Exception:
            # Session is shared between repositories
            # Ensure atomicity of this operation
            self.game_unit_of_work.repository.session.rollback()
            raise

        self.game_unit_of_work.repository.session.commit()

        return GuessGameStatusReadModel.from_entity(
            entity=guess,
            game_status=game.status,
        )
