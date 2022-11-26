import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_view(request):
    recipes = Recipe.objects.filter(is_published=False,
                                    author=request.user).order_by('-id')
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': page_object,
            'pagination_range': pagination_range
        },
    )

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    id = POST.get('id')

    recipe = Recipe.objects.filter(is_published=False,
                                   author=request.user,
                                   id=id).first()

    if not recipe:
        messages.error(request, 'This recipe was not found.')
        raise Http404()

    recipe.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect(reverse('authors:dashboard'))
