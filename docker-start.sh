tmux new-session -d -s redis "redis-server"
tmux new-session -d -s celery "celery -A config worker -l DEBUG"
tmux new-session -d -s celery_beat "celery -A config worker -l DEBUG"
tmux new-session -d -s nginx "nginx"
python3 manage.py migrate
python3 manage.py collectstatic --noinput
mv django_static/ /var/www/django_static/
python3 manage.py runserver 0.0.0.0:8000