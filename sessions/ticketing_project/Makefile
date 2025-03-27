start:  
	docker-compose up -d --build --force-recreate

stop:  
	docker-compose down

migrate:  
	docker-compose run web poetry run python manage.py migrate

test:  
	docker-compose run web pytest tests/

createadmin:  
	docker-compose run web poetry run python manage.py createsuperuser

logs-web:
	docker-compose logs web
