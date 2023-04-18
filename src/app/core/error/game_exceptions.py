from app.core.error.base_exception import BaseError


class GameNotFoundError(BaseError):
    message = "Game does not exist."


class GameAlreadyExistsError(BaseError):
    message = "Game already exists"
