from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'assistant_app'

urlpatterns = [
    path('',
        views.BusinessProfileCreateView.as_view(),
        name='create_assistant',
    ),
]