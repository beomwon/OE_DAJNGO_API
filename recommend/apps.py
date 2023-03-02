from django.apps import AppConfig
from osyulraeng import settings
import os

class RecommendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommend'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import operator
            operator.start()
            settings.SCHEDULER_DEFAULT = False

    