FROM python:3.10

WORKDIR /opt/app

# Install Poetry
RUN pip install poetry
COPY Makefile /opt/app/

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY tests ./tests
COPY assets ./assets

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

CMD ["python3", "src/solution/main.py"]
