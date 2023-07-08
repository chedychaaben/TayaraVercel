from django.contrib import admin
from .models import Annonce, AnnonceImage, Event
# Register your models here.

admin.site.register(Annonce)
admin.site.register(AnnonceImage)
admin.site.register(Event)