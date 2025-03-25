start:  
	docker-compose up -d

stop:  
	docker-compose down

migrate:  
	docker-compose run web python manage.py migrate

test:  
	docker-compose run web pytest tests/

createadmin:  
	docker-compose run web python manage.py createsuperuser