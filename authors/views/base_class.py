from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class BaseClassView(View):
    recipe = None

    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html',
                      context={
                          'form': form,
                      })
