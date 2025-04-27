up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

migrations:
	docker exec -ti django_core python manage.py makemigrations

migrate:
	docker exec -ti django_core python manage.py migrate

lint:
	black .
	isort .

superuser:
	docker exec -ti django_core python manage.py createsuperuser

.DEFAULT_GOAL := up
