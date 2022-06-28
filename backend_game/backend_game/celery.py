from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_game.settings')

app = Celery('backend_game')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()