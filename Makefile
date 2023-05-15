install:
	pip install -r requirements.txt && \
	python manage.py migrate && \
	python ./backend/pugorugh/scripts/data_import.py

gunicorn_dev:
	gunicorn -c gunicorn/dev.py

run:
	python manage.py runserver

run_prod:
	gunicorn -c gunicorn/prod.py