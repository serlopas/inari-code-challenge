from fastapi import Depends, status, HTTPException

from app.core.error.game_exceptions import GameNotFoundError
from app.mastermind.game.dependencies import get_retrieve_game_use_case
from app.mastermind.game.domain.entities.game_query_model import GameReadModel
from app.mastermind.game.presentation.routes.games_router import router
from app.mastermind.game.service.game_service import GameService
from app.mastermind.game.unit_of_work.use_cases.retrieve_game_use_case import RetrieveGameUseCase


@router.get(
    "/{id}/",
    response_model=GameReadModel,
    status_code=status.HTTP_200_OK,
)
def retrieve_game(id: str, retrieve_game_use_case: RetrieveGameUseCase = Depends(get_retrieve_game_use_case)):
    try:
        game = GameService.retrieve_game(id, retrieve_game_use_case)
    except GameNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return game
