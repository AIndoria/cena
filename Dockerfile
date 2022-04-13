###############################################
# Base Image
###############################################
FROM python:3.10-slim as python-base

ENV CENA_HOME="/app"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# create user account
RUN useradd -u 911 -U -d $CENA_HOME -s /bin/bash abc \
    && usermod -G users abc \
    && mkdir $CENA_HOME

###############################################
# Builder Image
###############################################
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev \
    libwebp-dev \
    # LDAP Dependencies
    libsasl2-dev libldap2-dev libssl-dev \
    gnupg gnupg2 gnupg1 \
    && pip install -U --no-cache-dir pip

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.6
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install -E pgsql --no-dev

###############################################
# Development Image
###############################################
FROM python-base as development
ENV PRODUCTION=false
ENV TESTING=false

# copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# copy backend
COPY ./cena $CENA_HOME/cena
COPY ./poetry.lock ./pyproject.toml $CENA_HOME/

# Alembic
COPY ./alembic $CENA_HOME/alembic
COPY ./alembic.ini $CENA_HOME/

# venv already has runtime deps installed we get a quicker install
WORKDIR $CENA_HOME
RUN . $VENV_PATH/bin/activate && poetry install
WORKDIR /

RUN chmod +x $CENA_HOME/cena/run.sh
ENTRYPOINT $CENA_HOME/cena/run.sh "reload"

###############################################
# CRFPP Image
###############################################
FROM hkotel/crfpp as crfpp

RUN echo "crfpp-container"

###############################################
# Production Image
###############################################
FROM python-base as production
ENV PRODUCTION=true
ENV TESTING=false

ARG COMMIT
ENV GIT_COMMIT_HASH=$COMMIT

# curl for used by healthcheck
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# copy CRF++ Binary from crfpp
ENV CRF_MODEL_URL=https://github.com/cena-recipes/nlp-model/releases/download/v1.0.0/model.crfmodel

ENV LD_LIBRARY_PATH=/usr/local/lib
COPY --from=crfpp /usr/local/lib/ /usr/local/lib
COPY --from=crfpp /usr/local/bin/crf_learn /usr/local/bin/crf_learn
COPY --from=crfpp /usr/local/bin/crf_test /usr/local/bin/crf_test

# copy backend
COPY ./cena $CENA_HOME/cena
COPY ./poetry.lock ./pyproject.toml $CENA_HOME/
COPY ./gunicorn_conf.py $CENA_HOME

# Alembic
COPY ./alembic $CENA_HOME/alembic
COPY ./alembic.ini $CENA_HOME/

# venv already has runtime deps installed we get a quicker install
WORKDIR $CENA_HOME
RUN . $VENV_PATH/bin/activate && poetry install -E pgsql --no-dev
WORKDIR /

# Grab CRF++ Model Release
RUN curl -L0 $CRF_MODEL_URL --output $CENA_HOME/cena/services/parser_services/crfpp/model.crfmodel

VOLUME [ "$CENA_HOME/data/" ]
ENV APP_PORT=9000

EXPOSE ${APP_PORT}

HEALTHCHECK CMD curl -f http://localhost:${APP_PORT}/docs || exit 1

RUN chmod +x $CENA_HOME/cena/run.sh
ENTRYPOINT $CENA_HOME/cena/run.sh
