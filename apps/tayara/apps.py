from django.apps import AppConfig
from jobs import updater


class TayaraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tayara'
    '''
    def ready(self):
    	updater.start()
    '''