start:
	COMPOSE_BAKE=True docker compose up -d --force-recreate --build

down:
	docker compose down --volumes

test:
	docker compose run --rm --entrypoint="" api poetry run pytest
	
logs:
	docker compose logs -f

api-logs:
	docker compose logs -f api
