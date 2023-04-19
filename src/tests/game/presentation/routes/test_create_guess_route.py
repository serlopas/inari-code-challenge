from unittest import mock

from starlette import status

from app.core.error.game_exceptions import GameNotFoundError, GameAlreadyFinishedError
from app.core.error.guess_exceptions import GuessSizeNotValid, GuessCombinationNotValid
from app.mastermind.game.presentation.schemas.guess_schemas import CreateGuessModel
from tests.factories.game_factory import GamesFactory


class TestCreateGuess:
    def test_create_guess(self, client, guess_code, session):
        game = GamesFactory()
        payload = CreateGuessModel(guess_code=guess_code).dict()

        response = client.post(f"/games/{game.id}/guesses/", json=payload)
        body = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in body
        assert "guess_code" in body
        assert "white_pegs" in body
        assert "black_pegs" in body
        assert "game_id" in body
        assert "created_at" in body
        assert "game_status" in body

    def test_create_guess_game_not_found(self, client, guess_code, session, faker):
        payload = CreateGuessModel(guess_code=guess_code).dict()

        with mock.patch(
            "app.mastermind.game.domain.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__",
            side_effect=GameNotFoundError,
        ):
            response = client.post(f"/games/{faker.uuid4()}/guesses/", json=payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_guess_incorrect_length(self, client, guess_code, session):
        game = GamesFactory()
        payload = CreateGuessModel(guess_code=guess_code).dict()

        with mock.patch(
            "app.mastermind.game.domain.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__",
            side_effect=GuessSizeNotValid,
        ):
            response = client.post(f"/games/{game.id}/guesses/", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == GuessSizeNotValid.message

    def test_create_guess_incorrect_combination(self, client, guess_code, session):
        game = GamesFactory()
        payload = CreateGuessModel(guess_code=guess_code).dict()

        with mock.patch(
            "app.mastermind.game.domain.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__",
            side_effect=GuessCombinationNotValid,
        ):
            response = client.post(f"/games/{game.id}/guesses/", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == GuessCombinationNotValid.message

    def test_create_guess_game_already_finished(self, client, guess_code, session):
        game = GamesFactory()
        payload = CreateGuessModel(guess_code=guess_code).dict()

        with mock.patch(
            "app.mastermind.game.domain.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__",
            side_effect=GameAlreadyFinishedError,
        ):
            response = client.post(f"/games/{game.id}/guesses/", json=payload)

        assert response.status_code == status.HTTP_423_LOCKED
        assert response.json()["detail"] == GameAlreadyFinishedError.message

    def test_create_guess_raises_exception(self, client, guess_code, session):
        game = GamesFactory()
        payload = CreateGuessModel(guess_code=guess_code).dict()

        with mock.patch(
            "app.mastermind.game.domain.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__",
            side_effect=Exception,
        ):
            response = client.post(f"/games/{game.id}/guesses/", json=payload)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
