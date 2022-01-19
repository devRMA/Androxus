FROM python:3.10.2

ARG DEVELOPMENT

ENV DEVELOPMENT=${DEVELOPMENT} \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# System deps
RUN apt-get update; \
    apt-get upgrade -y; \
    pip install "poetry==$POETRY_VERSION"; \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    apt-get clean -y && rm -rf /var/lib/apt/lists/*;

WORKDIR /usr/src/androxus

# Setting up the user
RUN useradd -ms /bin/bash androxus;

# Copy only requirements, to cache them in docker layer
COPY ./poetry.lock ./pyproject.toml /usr/src/androxus/

# Project initialization
RUN poetry config virtualenvs.create false; \
    poetry install $(test "$DEVELOPMENT" == false && echo "--no-dev") --no-interaction --no-ansi; \
    poetry update;

USER androxus

# Creating folders, and files for a project
COPY . .

ENTRYPOINT ["python", "main.py"]
