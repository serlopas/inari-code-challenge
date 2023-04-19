from app.core.error.base_exception import BaseError


class GameNotFoundError(BaseError):
    message = "Game does not exist."


class GameAlreadyFinishedError(BaseError):
    message = "Game already finished"
