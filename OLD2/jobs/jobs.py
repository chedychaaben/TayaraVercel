from django.conf import settings
import requests
import json
import random 

def schedule_api():
    # This function is triggered every 10 minutes :)
    try:
        from apps.tayara.views import jobFN
        jobFN()
    except:
        pass