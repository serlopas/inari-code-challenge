from unittest import mock

from app.mastermind.game.service.game_service import GameService


class TestGameService:
    def test_create_game(self, create_game_use_case):
        with mock.patch(
            "app.mastermind.game.unit_of_work.use_cases.create_game_use_case.CreateGameUseCaseImpl.__call__"
        ) as use_case_mock:
            GameService.create_game(create_game_use_case)

        use_case_mock.assert_called_once()

    def test_retrieve_game(self, retrieve_game_use_case, faker):
        with mock.patch(
            "app.mastermind.game.unit_of_work.use_cases.retrieve_game_use_case.RetrieveGameUseCaseImpl.__call__"
        ) as use_case_mock:
            GameService.retrieve_game(faker.uuid4(), retrieve_game_use_case)

        use_case_mock.assert_called_once()

    def test_create_guess(self, create_guess_use_case, guess_code, faker):
        with mock.patch(
            "app.mastermind.game.unit_of_work.use_cases.create_guess_use_case.CreateGuessUseCaseImpl.__call__"
        ) as use_case_mock:
            GameService.create_guess(faker.uuid4(), guess_code, create_guess_use_case)

        use_case_mock.assert_called_once()
