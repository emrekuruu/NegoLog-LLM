FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y xdg-utils curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry configuration
COPY pyproject.toml ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["python", "run.py", "tournament_example.yaml"]
