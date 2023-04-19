from unittest import mock

from starlette import status

from app.core.error.game_exceptions import GameNotFoundError
from tests.factories.game_factory import GamesFactory
from tests.factories.guess_factory import GuessesFactory


class TestRetrieveGame:
    def test_retrieve_game(self, client, session):
        game = GamesFactory()

        response = client.get(f"/games/{game.id}")
        body = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in body
        assert "code" in body
        assert "status" in body
        assert "tries" in body
        assert "max_tries" in body
        assert "guesses" in body
        assert "created_at" in body

    def test_retrieve_game_with_guesses(self, client, session):
        game = GuessesFactory().game

        response = client.get(f"/games/{game.id}")
        body = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert "id" in body
        assert "code" in body
        assert "status" in body
        assert "tries" in body
        assert "max_tries" in body
        assert "guesses" in body
        assert len(body["guesses"]) == 1
        assert "created_at" in body

    def test_retrieve_game_internal_error(self, client, session, faker):
        with mock.patch("app.mastermind.game.service.game_service.GameService.retrieve_game", side_effect=Exception):
            response = client.get(f"/games/{faker.uuid4()}")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_retrieve_game_not_found(self, client, faker):
        with mock.patch(
            "app.mastermind.game.service.game_service.GameService.retrieve_game", side_effect=GameNotFoundError
        ):
            response = client.get(f"/games/{faker.uuid4()}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
