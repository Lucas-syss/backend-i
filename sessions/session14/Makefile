
start:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py migrate

migration:
	poetry run python manage.py makemigrations

createsuperuser:
	poetry run python manage.py createsuperuser

newapp:
	poetry run python manage.py startapp $(app)
	@# to execute run `make newapp app=cenas`

tests:
	poetry run pytest -vvv

compose.migrate:
	docker compose run --rm web poetry run python manage.py migrate