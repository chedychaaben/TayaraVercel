#static files and media files importation
from django.conf import settings
from django.conf.urls.static import static
#static files and media files importation

from django.contrib import admin
from django.urls import path, include
import apps.tayara.views as tayara
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'),name='homepage'), # React build renderer
    path('api/', include("apps.api.urls")),
    path('auth/', include("apps.users.urls")),
    path('createAnnonce/', tayara.createAnnonce, name='createAnnonce'),
    path('deleteAnnonce/', tayara.deleteAnnonce, name='deleteAnnonce'),
    path('loginOnTayara/', tayara.loginOnTayara, name='loginOnTayara'),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)