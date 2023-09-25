Run docker compose:
	docker-compose up
	docker-compose up --build

Run_docker-compose-local:
	docker-compose -f docker-compose-local.yml up

Rebuild docker-compose:
	docker-compose -f docker-compose-local.yml up --build

Start project:
	django-admin startproject projectname

Start App:
	python3 manage.py startapp appname

Linters:
	isort . tests
	black . tests
	flake8 . tests
	run mypy .

#Tests
Run tests:
	docker exec -it api-gateway pytest -v -s

Coverage:
	docker exec -it api-gateway coverage run -m pytest
	docker exec -it api-gateway coverage report -m

#Django
Make migrations:
	docker exec -it api-gateway python3 manage.py makemigrations

Use migrations:
	docker exec -it api-gateway python3 manage.py migrate

Use migrations:
	docker exec -it api-gateway python3 manage.py shell

Create superuser:
	docker exec -it api-gateway python3 manage.py createsuperuser

#DB
Database:
	docker exec -it py-db bash
	psql -U postgres

Database:
	docker exec -it py-db bash -c "su postgres -c 'psql'"

Force drop database:
	DROP DATABASE api_gateway_db WITH (FORCE);

Redis:
	docker exec -it api-gateway-redis redis-cli

#Poetry
Poetry add:
	docker exec -it api-gateway poetry add "name of package"

Poetry remove:
	docker exec -it api-gateway poetry add "name of package"

#Celery
celery(worker):
	celery -A app.celery.tasks worker -l info

beat:
	celery -A app.celery.tasks beat -l info

flower:
	celery -A app.celery.tasks flower --address=0.0.0.0

rebuild consumer:
	docker-compose up -d --build api-gateway-consumer