from django.conf import settings
import requests
import json
import random
from apps.tayara.views import scheduled_job


def schedule_api():
    # This function is triggered every 10 minutes :)
    
    scheduled_job()