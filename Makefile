install:
	@poetry install

lint:
	@poetry run flake8 --exclude=*migrations/* task_manager

test:
	@poetry run coverage run manage.py test
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

collectstatic:
	@poetry run python manage.py collectstatic

start:
	@poetry run gunicorn task_manager.wsgi

prepare: collectstatic migrate




.PHONY : install lint test check selfcheck deploy public migrate start collectstatic prepare