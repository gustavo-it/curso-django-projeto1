from django.urls import path

from . import views

# Da pasta em que eu estou importe as views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),  # importando a view home
    path('recipes/<int:id>/', views.recipes, name="recipe"),
]
