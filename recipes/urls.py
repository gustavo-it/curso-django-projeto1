from django.urls import path

from . import views

urlpatterns = [
    path('', views.home), # Chamando a view home
    path('recipes/<int:id>/', views.recipe)
]
