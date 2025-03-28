FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /app  

COPY pyproject.toml poetry.lock /app/

RUN poetry install -n

COPY . .

RUN poetry run python manage.py collectstatic --noinput

VOLUME [ "/app" ]

CMD [ "poetry","run","uvicorn","ticketing_project.asgi:application","--host","0.0.0.0","--port","8000" ]