FROM python:3.11.4-slim

ENV HOMEDIR=/app \
  TERM=vt100 \
  C_FORCE_ROOT=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app

ARG ENV

WORKDIR $HOMEDIR

# hadolint ignore=DL3008,DL3013
RUN apt-get update -y --fix-missing \
  && apt-get install --no-install-recommends -y libgnutls30 liblz4-1 openssl libssl1.1 libexpat1=* \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean \
  && pip install --no-cache-dir --upgrade pip poetry==1.3.2 \
  && poetry config virtualenvs.create false \
  && poetry self add poetry-bumpversion

COPY src/pyproject.toml $HOMEDIR/pyproject.toml
COPY src/poetry.lock $HOMEDIR/poetry.lock
RUN if [ "$ENV" = "local" ] ; then poetry install ; else poetry install --no-dev ; fi

COPY src $HOMEDIR/

CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:80", "--reload", "--access-logfile", "-"]

EXPOSE 80
