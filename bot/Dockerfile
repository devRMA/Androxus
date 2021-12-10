FROM python:3.10.1

# python
ENV PYTHONFAULTHANDLER=1 \
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

# Setting up proper permissions
RUN groupadd -r androxus; \
    useradd -d /usr/src/androxus -r -g androxus androxus; \
    chown androxus:androxus -R /usr/src/androxus;

# Copy only requirements, to cache them in docker layer
COPY --chown=androxus:androxus ./poetry.lock ./pyproject.toml /usr/src/androxus/

# Project initialization
RUN poetry config virtualenvs.create false; \
    poetry install --no-interaction --no-ansi;

USER androxus

# Creating folders, and files for a project
COPY --chown=androxus:androxus . /usr/src/androxus/

ENTRYPOINT ["python", "main.py"]
