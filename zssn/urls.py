from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('', include('geral.urls', namespace='geral')),
    path('admin/', admin.site.urls),
]