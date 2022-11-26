from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from recipes.models import Recipe

from ..forms.recipe_form import AuthorsRecipeForm


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            id=id,
        )

        form = AuthorsRecipeForm(data=request.POST or None,
                                 files=request.POST or None,
                                 instance=recipe)

        if not recipe:
            raise Http404()

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.authors = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(id,)))
        return render(request, 'authors/pages/dashboard_recipe.html', context={
            'form': form,
        })
