from app.core.services.base_query_service import BaseQueryService

from app.mastermind.game.domain.entities.guess_query_model import GuessReadModel


class GuessQueryService(BaseQueryService[GuessReadModel]):
    pass
