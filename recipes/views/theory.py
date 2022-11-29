from django.shortcuts import render
from django.views import View


class Theory(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'recipes/pages/theory.html')
