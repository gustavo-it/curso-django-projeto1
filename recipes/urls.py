from django.urls import path

from recipes.views import contato, home

urlpatterns = [
    path('', home), # Chamando a view home
    path('contato/', contato)
]
