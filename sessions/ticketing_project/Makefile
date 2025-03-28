start:  
	poetry run python manage.py runserver 

stop:  
	docker-compose down

migrate:
	poetry run python manage.py migrate
 
migrations:
	poetry run python manage.py makemigrations $(app)

compose.start:
	docker compose up --build --force-recreate

compose.migrate:  
	docker compose run --rm web poetry run python manage.py migrate

compose.migrations:  
	docker compose run --rm web poetry run python manage.py makemigrations

test:  
	docker-compose run web pytest tests/

createadmin:  
	docker-compose run web poetry run python manage.py createsuperuser

logs-web:
	docker-compose logs web

compose.collectstatic:
	docker compose exec web poetry run python manage.py collectstatic --noinput