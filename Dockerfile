FROM python:3.9.7-slim
SHELL ["/bin/bash", "-c"]

RUN apt update && \
    apt upgrade -y && \
    mkdir /srv/app && \
    useradd -d /srv/app app && \
    mkdir -p /srv/app/configs/ && \
    chown app:app /srv/app

WORKDIR /srv/app
COPY --chown=app:app data data
COPY --chown=app:app telegram_clock telegram_clock
COPY --chown=app:app configs/config_example.yaml configs/config.yaml
COPY --chown=app:app poetry.lock poetry.lock
COPY --chown=app:app pyproject.toml pyproject.toml
COPY --chown=app:app docker/init_session.sh init_session.sh

USER app

RUN python3 -m venv venv && \
    source ./venv/bin/activate && \
    pip install -U pip && \
    pip install poetry && \
    poetry install

ENTRYPOINT [ "/srv/app/venv/bin/python", "-m", "telegram_clock"]