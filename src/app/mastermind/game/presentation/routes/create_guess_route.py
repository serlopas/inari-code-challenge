from fastapi import Depends, status, HTTPException

from app.core.error.game_exceptions import GameNotFoundError, GameAlreadyFinishedError
from app.core.error.guess_exceptions import GuessSizeNotValid, GuessCombinationNotValid
from app.mastermind.game.dependencies import get_create_guess_use_case
from app.mastermind.game.domain.entities.guess_query_model import GuessGameStatusReadModel
from app.mastermind.game.domain.use_cases.create_guess_use_case import CreateGuessUseCase
from app.mastermind.game.presentation.routes.games_router import router
from app.mastermind.game.presentation.schemas.guess_schemas import CreateGuessModel


@router.post(
    "/{id}/guesses/",
    response_model=GuessGameStatusReadModel,
    status_code=status.HTTP_201_CREATED,
)
def create_guess(
    id: str,
    data: CreateGuessModel,
    create_guess_use_case: CreateGuessUseCase = Depends(get_create_guess_use_case),
):
    try:
        guess_result = create_guess_use_case(
            (
                id,
                data.guess_code,
            )
        )
    except GameNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except GuessSizeNotValid as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except GuessCombinationNotValid as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except GameAlreadyFinishedError as e:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=e.message,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return guess_result
