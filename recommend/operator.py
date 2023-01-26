from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import saveTeamAndMenu
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.jobstores import register_events

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    register_events(scheduler)

    scheduler.add_job(
        saveTeamAndMenu,
        trigger=CronTrigger(hour="17", minute="00")
    )

    scheduler.start()