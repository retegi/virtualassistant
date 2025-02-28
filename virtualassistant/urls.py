from django.contrib import admin
from django.urls import path, include
from applications.assistant.views import assistant_view
from django.urls import path
from applications.home.views import create_payment, execute_payment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.home.urls')),
    path('assistant/', include('applications.assistant.urls')),
    path('accounts/', include('allauth.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('<str:assistant_url_name>/', assistant_view, name='assistant_detail'),
    path("paypal/payment/<str:plan_type>/", create_payment, name="paypal_payment"),
    path("paypal/execute/<str:plan_type>/", execute_payment, name="paypal_execute"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)