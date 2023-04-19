from app.core.error.base_exception import BaseError


class GuessSizeNotValid(BaseError):
    message = "Size of the guess code is not valid"


class GuessCombinationNotValid(BaseError):
    message = "Some of the colors in the guess code are not valid"
