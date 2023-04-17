import sentry_sdk

from app.settings.base import get_settings


def init_sentry_service() -> None:
    """
    Configure the Sentry SDK

    To configure the Sentry SDK, initialize it before your app has been initialized.
    https://docs.sentry.io/platforms/python/guides/fastapi/

    :return: None
    """
    sentry_sdk.init(
        release=get_settings().SENTRY_RELEASE,
        dsn=get_settings().SENTRY_DSN,
        environment=get_settings().SENTRY_ENVIRONMENT,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=get_settings().SENTRY_TRACES_SAMPLE_RATE,
    )
