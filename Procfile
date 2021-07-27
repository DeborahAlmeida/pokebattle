web: gunicorn pokebattle.wsgi --chdir backend --limit-request-line 8188 --log-file -
worker: celery -A pokebattle --workdir backend -B --loglevel=info worker
