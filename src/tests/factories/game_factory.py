import random
from datetime import datetime

import factory

from app.core.enums.enums import ColorsEnum, GameStatusEnum
from app.mastermind.game.data.models.models import Game
from app.settings.base import get_settings
from tests.factories.base_factory import BaseFactory


class GamesFactory(BaseFactory):
    id = factory.Faker("uuid4")
    code = "".join(random.choices(list(ColorsEnum), k=get_settings().CODE_SIZE))
    status = GameStatusEnum.in_progress
    tries = 0
    max_tries = get_settings().MAX_TRIES
    created_at = datetime.now()

    class Meta:
        model = Game
