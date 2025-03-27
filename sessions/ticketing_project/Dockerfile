FROM python:3.12-slim

WORKDIR /app  

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-interaction

COPY . .

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]