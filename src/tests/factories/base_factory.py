import factory

from tests.conftest import session_for_factory


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_COMMIT

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        cls._meta.sqlalchemy_session = session_for_factory.get()
        return super()._create(model_class, *args, **kwargs)
