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

    path('formulario/', views.formulario_contactar, name='formulario_contactar'),

    path('tarifa/',
        views.TarifaPageView.as_view(),
        name='tarifa',
    ),
    path('tarifa-anual/',
        views.TarifaAnualPageView.as_view(),
        name='tarifa_anual',
    ),
    path('tarifa-mensual/',
        views.TarifaMensualPageView.as_view(),
        name='tarifa_mensual',
    ),
    path('dashboard/',
        views.DashboardView.as_view(),
        name='dashboard',
    ),

    path('assistant/<int:pk>/', views.AssistantProfileDetailView.as_view(), name='assistant_detail'),
    path('assistant-create/', views.AssistantCreateView.as_view(), name='assistant_create'),
    path('assistant-update/<int:pk>', views.AssistantUpdateView.as_view(), name='assistant_update'),
    path('assistant-delete/<int:pk>', views.AssistantDeleteView.as_view(), name='assistant_delete'),

    #Productos
    path("create-product/<int:business_id>/", views.CreateProductView.as_view(), name="create_product"),
    path("business/<int:business_id>/products/", views.ProductListView.as_view(), name="product_list"),
    path("edit-product/<int:pk>/", views.UpdateProductView.as_view(), name="update_product"),
    path("delete-product/<int:pk>/", views.DeleteProductView.as_view(), name="delete_product"),

    #Servicios
    path("create-service/<int:business_id>/", views.CreateServiceView.as_view(), name="create_service"),
    path("business/<int:business_id>/services/", views.ServiceListView.as_view(), name="service_list"),
    path("edit-service/<int:pk>/", views.UpdateServiceView.as_view(), name="update_service"),
    path("delete-service/<int:pk>/", views.DeleteServiceView.as_view(), name="delete_service"),

    #FAQ Preguntas y respuestas
    path("create-faq/<int:business_id>/", views.FAQCreateView.as_view(), name="create_faq"),
    path("business/<int:business_id>/faq/", views.FAQListView.as_view(), name="list_faq"),
    path("edit-faq/<int:pk>/", views.FAQUpdateView.as_view(), name="update_faq"),
    path("delete-faq/<int:pk>/", views.FAQDeleteView.as_view(), name="delete_faq"),

]