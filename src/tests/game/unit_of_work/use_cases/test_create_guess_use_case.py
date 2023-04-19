import random
from unittest import mock

import pytest

from app.core.enums.enums import GameStatusEnum
from app.core.error.game_exceptions import GameNotFoundError, GameAlreadyFinishedError
from app.core.error.guess_exceptions import GuessSizeNotValid, GuessCombinationNotValid
from app.mastermind.game.domain.entities.guess_query_model import GuessGameStatusReadModel
from app.mastermind.game.repository.sqlalchemy.models.models import Guess
from app.mastermind.game.unit_of_work.use_cases.create_guess_use_case import CreateGuessUseCaseArgs
from app.settings.base import get_settings
from tests.factories.game_factory import GamesFactory


class TestCreateGuessUseCaseImpl:
    def test_call(self, create_guess_use_case, guess_code, session):
        game = GamesFactory()

        guess_result = create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=guess_code))
        assert isinstance(guess_result, GuessGameStatusReadModel)

        guess = session.get(Guess, guess_result.id)
        assert guess is not None
        assert len(game.guesses) == 1

        assert guess_result.guess_code == guess_code
        assert guess_result.game_id == game.id

    def test_call_game_not_exist(self, create_guess_use_case, guess_code, session, faker):
        with pytest.raises(GameNotFoundError):
            create_guess_use_case(CreateGuessUseCaseArgs(game_id=faker.uuid4(), guess_code=guess_code))

    def test_call_game_already_finished(self, create_guess_use_case, guess_code, session):
        game = GamesFactory(status=random.choice((GameStatusEnum.won, GameStatusEnum.lost)))

        with pytest.raises(GameAlreadyFinishedError):
            create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=guess_code))

    def test_call_guess_incorrect_length(self, create_guess_use_case, guess_code, session):
        game = GamesFactory()

        with pytest.raises(GuessSizeNotValid):
            create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=f"{guess_code}a"))

    def test_call_guess_incorrect_color(self, create_guess_use_case, session):
        game = GamesFactory()
        guess_code = "".join(random.choices("$!=@", k=get_settings().CODE_SIZE))

        with pytest.raises(GuessCombinationNotValid):
            create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=guess_code))

    def test_call_game_won(self, create_guess_use_case, session):
        game = GamesFactory()
        guess_result = create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=game.code))

        assert guess_result.guess_code == game.code
        assert guess_result.black_pegs == get_settings().CODE_SIZE
        assert guess_result.white_pegs == 0
        assert guess_result.game_status == GameStatusEnum.won
        assert game.status == GameStatusEnum.won

    def test_call_game_lost(self, create_guess_use_case, guess_code, session):
        game = GamesFactory(tries=get_settings().MAX_TRIES - 1)
        guess_result = create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=guess_code))

        assert guess_result.guess_code == guess_code
        assert guess_result.game_status == GameStatusEnum.lost
        assert game.status == GameStatusEnum.lost

    def test_call_raise_exception(self, create_guess_use_case, guess_code, session):
        game = GamesFactory()

        with mock.patch.object(
            create_guess_use_case.game_unit_of_work.repository.session, "rollback"
        ) as rollback_mock, mock.patch.object(
            create_guess_use_case.game_unit_of_work.repository, "update"
        ) as update_mock, pytest.raises(
            Exception
        ):
            update_mock.side_effect = Exception
            create_guess_use_case(CreateGuessUseCaseArgs(game_id=game.id, guess_code=guess_code))

        rollback_mock.assert_called_once()
