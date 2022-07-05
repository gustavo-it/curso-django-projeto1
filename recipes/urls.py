from django.urls import path

from . import views

# Da pasta em que eu estou importe as views

urlpatterns = [
    path('', views.home),  # importando a view home
    path('recipes/<int:id>/', views.recipes),
]
