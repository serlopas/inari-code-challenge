from app.core.services.base_query_service import BaseQueryService

from app.mastermind.game.domain.entities.game_query_model import GameReadModel


class GameQueryService(BaseQueryService[GameReadModel]):
    pass
