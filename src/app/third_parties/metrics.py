from prometheus_fastapi_instrumentator import Instrumentator, PrometheusFastApiInstrumentator


def create_prometheus_instrumentator(app) -> PrometheusFastApiInstrumentator:
    """
    Add prometheus instrumentator middleware to the FastApi app
    :param app: FastApi app
    :return: PrometheusFastApiInstrumentator
    """
    return Instrumentator().instrument(app)


async def expose_metric_service(app, prometheus_instrumentator) -> None:
    """
    Expose FastApi metrics for a prometheus consumer

    https://github.com/trallnag/prometheus-fastapi-instrumentator.

    :param app: FastApi app
    :param prometheus_instrumentator: PrometheusFastApiInstrumentator
    :return: None
    """
    prometheus_instrumentator.expose(app)
