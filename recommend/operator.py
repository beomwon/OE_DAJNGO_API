from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import saveTeamAndMenu

def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour=2, minute=50, name='saveTeamAndMenu')
    def auto_check():
        saveTeamAndMenu()
    scheduler.start()