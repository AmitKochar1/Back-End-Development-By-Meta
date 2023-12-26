from django.urls import path
from . import views 

urlpatterns = [
    path("home/<str:dish>", views.menuitems, name="menuitems"),
]