from django.contrib import admin
from django.urls import path, include
from applications.assistant.views import assistant_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.home.urls')),
    path('assistant/', include('applications.assistant.urls')),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('<str:assistant_url_name>/', assistant_view, name='assistant_detail'),
]
