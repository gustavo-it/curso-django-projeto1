from django.shortcuts import render
from django.views import View

from ..models import Recipe


class Theory(View):
    def get(self, *args, **kwargs):
        recipes = Recipe.objects.get_published()
        return render(self.request, 'recipes/pages/theory.html', context={
            'recipes': recipes
        })
