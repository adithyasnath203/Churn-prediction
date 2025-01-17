import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'main.settings')

app = Celery ('django_with_celery')

app.config_from_object('django.conf:settings' , namespace='CELERY')

app.autodiscover_tasks()
