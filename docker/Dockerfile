FROM python:3.11.2-slim-buster AS runtime

WORKDIR /app

RUN pip install --upgrade pip

# Install cron
RUN apt-get update && apt-get -y install cron

# Install poetry
RUN pip install poetry

# Copy only requirements to cache in docker layer
COPY pyproject.toml poetry.lock /app/

# Install packages, do not create virtualenv in docker
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./main.py .
COPY ./src ./src

# Set up cron job
COPY ./cron .
RUN crontab /app/cron
RUN touch /var/log/cron.log


# ENTRYPOINT poetry run python main.py

# Start cron job, clear log (from any prev runs) and tail it
ENTRYPOINT cron && echo "" > /var/log/cron.log && tail -f /var/log/cron.log