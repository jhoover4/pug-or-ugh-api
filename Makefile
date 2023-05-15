install:
	pip install -r requirements.txt && \
	python manage.py migrate && \
	python ./backend/pugorugh/scripts/data_import.py

run:
	python manage.py runserver