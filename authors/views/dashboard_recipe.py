import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from recipes.models import Recipe
from utils.pagination import make_pagination

from ..forms.recipe_form import AuthorsRecipeForm
from .base_class import BaseClassView

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(BaseClassView):
    def get(self, request, id):
        recipe = self.get_recipe(id)
        form = AuthorsRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id):
        recipe = self.get_recipe(id)

        form = AuthorsRecipeForm(data=request.POST or None,
                                 files=request.POST or None,
                                 instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = self.request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(
                self.request, 'Sua receita foi atualizada com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(id,)))

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeNew(BaseClassView):
    def get(self, request):
        form = AuthorsRecipeForm()
        return self.render_recipe(form)

    def post(self, request):
        form = AuthorsRecipeForm(
            data=request.POST or None,
            files=request.FILES or None
        )

        if form.is_valid():
            recipe: Recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita acaba de ser cadastrada. ' +
                             'Aguarde um administrador aprova-lá')
            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(recipe.id,)))

        return render(request, 'authors/pages/dashboard_recipe.html', context={
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_new')
        })


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(BaseClassView):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'A receita foi apagada com sucesso!')
        return redirect(reverse('authors:dashboard'))


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardView(View):
    def get(self, request):
        recipes = Recipe.objects.filter(is_published=False,
                                        author=request.user).order_by(
                                            '-id'
        )
        page_object, pagination_range = make_pagination(
            request, recipes, PER_PAGE)
        return render(request, 'authors/pages/dashboard.html', context={
            'recipes': page_object,
            'pagination_range': pagination_range
        })
