from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('chatapi/', include('chatapi.urls')),
    path('auth/', include('custom_auth.urls')),
=======
    path('api/', include('chatapi.urls')),
>>>>>>> 08baa90 (Initialized a new postgres database)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
