import enum


class GameStatusEnum(str, enum.Enum):
    lost = "lost"
    won = "won"
    in_progress = "in_progress"


class ColorsEnum(str, enum.Enum):
    blue = "b"
    red = "r"
    green = "g"
    yellow = "y"
    white = "w"
    orange = "o"
