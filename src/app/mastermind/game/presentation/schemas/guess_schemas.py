from pydantic import BaseModel


class CreateGuessModel(BaseModel):
    guess_code: str
