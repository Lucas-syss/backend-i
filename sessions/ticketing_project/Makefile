stop:  
	docker-compose down

compose.start:
	docker compose up --build --force-recreate

compose.migrate:  
	docker compose run --rm web poetry run python manage.py migrate

compose.migrations:  
	docker compose run --rm web poetry run python manage.py makemigrations

test:  
	docker compose run --rm web poetry run python manage.py test

createadmin:  
	docker compose exec web poetry run python manage.py createsuperuser

logs-web:
	docker compose logs web

compose.collectstatic:
	docker compose exec web poetry run python manage.py collectstatic --noinput

createusers:
	docker compose run web poetry run python manage.py shell -c "from tickets.models import User; \
	User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123', role='admin'); \
	User.objects.create_user(username='customer', email='customer@example.com', password='customer123', role='customer'); \
	User.objects.create_user(username='agent', email='agent@example.com', password='agent123', role='agent', is_staff=True); \
	print('Admin, Customer, and Agent users created successfully.')"