from django.contrib import admin
from .models import Annonce, AnnonceImage, AnnonceCreateProcess,AnnonceDeleteProcess , Task
# Register your models here.

admin.site.register(Annonce)
admin.site.register(AnnonceImage)
admin.site.register(AnnonceCreateProcess)
admin.site.register(AnnonceDeleteProcess)
admin.site.register(Task)