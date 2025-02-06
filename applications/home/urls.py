from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home_app'

urlpatterns = [
    path('',
        views.HomePageView.as_view(),
        name='home',
    ),
    path('tarifa/',
        views.TarifaPageView.as_view(),
        name='tarifa',
    ),
]