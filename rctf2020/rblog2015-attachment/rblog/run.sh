pip install -r requirements.txt
rm -rf db.sqlite3 */migrations/ */__pycache__/
python manage.py makemigrations posts
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; from os import getenv; User.objects.create_user(is_staff=True, username=getenv('BOT_NAME'), password=getenv('BOT_PASS')).save()"
python manage.py loaddata posts.json
gunicorn -c gunicorn_config.py rblog4.wsgi