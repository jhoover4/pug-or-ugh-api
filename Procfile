release: python backend/manage.py migrate --no-input
web: gunicorn --pythonpath backend backend.wsgi --log-file -