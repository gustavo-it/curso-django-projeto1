from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html')
    #  Passando o caminho do template, lembre que por padrão o Django identifica a pasta templates


def recipes(request, id):
    return render(request, 'recipes/pages/home.html')
