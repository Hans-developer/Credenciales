from django.urls import path
from . import views



urlpatterns = [
    path('', views.Vista.as_view(), name='vista'),
    #path("generarpdf/", views.GenerarPdf.as_view(), name='generarpdf'),
]