from pydantic import Field

from app.core.error.base_exception import BaseError
from app.core.error.game_exceptions import GameNotFoundError, GameAlreadyExistsError


class ErrorMessageGameNotFound(BaseError):
    detail: str = Field(example=GameNotFoundError.message)


class ErrorMessageGameAlreadyExists(BaseError):
    detail: str = Field(example=GameAlreadyExistsError.message)
