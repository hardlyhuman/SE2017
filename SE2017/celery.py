
from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SE2017.settings')

app = Celery('SE2017')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

'''app.conf.beat_schedule = {
    'send-notification-every-single-minute': {
        'task': 'app1.tasks.send_notification',
        'schedule': crontab(minute='*/1',day_of_week='4'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}
'''
