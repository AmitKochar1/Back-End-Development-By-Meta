from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu-items/<int:pk>', views.single_item),
    path('secret/', views.secret_message),
    path('api-token-auth/', obtain_auth_token)
] 
