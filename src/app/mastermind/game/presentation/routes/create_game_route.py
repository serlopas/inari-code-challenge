from fastapi import Depends, status, APIRouter

from app.mastermind.game.dependencies import get_create_game_use_case
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.domain.use_cases.create_game_use_case import CreateGameUseCase

router = APIRouter()


@router.post(
    "/",
    response_model=GameReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_game(
    create_game_use_case: CreateGameUseCase = Depends(get_create_game_use_case),
):
    return create_game_use_case(None)
