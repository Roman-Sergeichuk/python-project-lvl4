install:
	@poetry install

lint:
	@poetry run flake8 --exclude=*migrations/* task_manager

test:
	@poetry run coverage run --source=task_manager --omit=*/migrations/* manage.py test --settings=task_manager.settings
	@poetry run coverage xml

selfcheck:
	@poetry check

check: selfcheck test lint

deploy:
	git push https://git.heroku.com/taskmanager-rs.git


public:
	@poetry build
	@poetry config repositories.dist https://test.pypi.org/legacy/
	@poetry publish -r dist

migrate:
	@poetry run python manage.py makemigrations
	@poetry run python manage.py migrate

start:
	@poetry run gunicorn task_manager.wsgi




.PHONY : install lint test deploy public migrate start