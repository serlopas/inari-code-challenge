from unittest import mock

from app.settings.base import get_settings
from app.third_parties.sentry import init_sentry_service


class TestInitSentryService:
    @mock.patch("sentry_sdk.init")
    def test_init_sentry_service(self, sentry_init_mock):
        init_sentry_service()

        sentry_init_mock.assert_called_once_with(
            release=get_settings().SENTRY_RELEASE,
            dsn=get_settings().SENTRY_DSN,
            environment=get_settings().SENTRY_ENVIRONMENT,
            traces_sample_rate=get_settings().SENTRY_TRACES_SAMPLE_RATE,
        )
