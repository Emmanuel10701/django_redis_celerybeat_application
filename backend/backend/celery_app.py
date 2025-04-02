import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_scheduled_stories': {
        'task': 'story_scheduler.tasks.check_scheduled_stories',
        'schedule': settings.CELERY_BEAT_CHECK_INTERVAL,
    },
}