from fastapi import Depends, status

from app.mastermind.game.dependencies import get_create_game_use_case
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.presentation.routes.games_router import router
from app.mastermind.game.service.game_service import GameService
from app.mastermind.game.unit_of_work.use_cases.create_game_use_case import CreateGameUseCase


@router.post(
    "/",
    response_model=GameReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_game(
    create_game_use_case: CreateGameUseCase = Depends(get_create_game_use_case),
):
    return GameService.create_game(create_game_use_case)
