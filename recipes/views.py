from django.shortcuts import render
from utils.recipes.factory import make_recipe  # importando a função


def home(request):
    return render(request, 'recipes/pages/home.html', context={'recipes': [make_recipe() for _ in range(10)]})
    #  Passando o caminho do template, lembre que por padrão o Django identifica a pasta templates
    #  Estamos passando no contexto a função de teste, executando uma list comprehension que gera 10 receitas


def recipes(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={'recipe': make_recipe()})
    #  Estamos passando a chave no singular, para que seja apresentado somente uma receita
