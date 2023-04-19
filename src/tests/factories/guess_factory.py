import random
from datetime import datetime

import factory

from app.core.enums.enums import ColorsEnum
from app.mastermind.game.repository.sqlalchemy.models.models import Guess
from app.settings.base import get_settings
from tests.factories.base_factory import BaseFactory
from tests.factories.game_factory import GamesFactory


class GuessesFactory(BaseFactory):
    id = factory.Faker("uuid4")
    guess_code = "".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE))
    white_pegs = factory.Faker("pyint", min_value=0, max_value=4)
    black_pegs = factory.Faker("pyint", min_value=0, max_value=4)
    game = factory.SubFactory(GamesFactory)
    created_at = datetime.now()

    class Meta:
        model = Guess
