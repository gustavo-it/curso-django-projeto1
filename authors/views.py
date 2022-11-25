import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from recipes.models import Recipe
from utils.pagination import make_pagination

from .forms import LoginForm, RegisterForm
from .forms.recipe_form import AuthorsRecipeForm

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def register_view(request):
    register_form_data = request.session.get("register_form_data", None)
    form = RegisterForm(register_form_data)

    return render(request,
                  'authors/pages/register_view.html',
                  context={
                      "form": form,
                      "form_action": reverse("authors:register_create")
                  })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session["register_form_data"] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "Your user is created, please log in.")

        del (request.session["register_form_data"])
        return redirect(reverse("authors:login"))

    return redirect("authors:register")


def login_view(request):
    form = LoginForm()
    return render(request,
                  'authors/pages/login.html',
                  context={
                      "form": form,
                      "form_action": reverse("authors:login_create")
                  })


def login_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )

        if authenticated_user is not None:
            messages.success(request, "Your logged in.")
            login(request, authenticated_user)
        else:
            messages.error(request, "Invalid credentials")
            return redirect(reverse('authors:login'))
    else:
        messages.error(request, "Invalid username or password")
        return redirect(reverse('authors:login'))

    return redirect(reverse('authors:dashboard'))


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    logout(request)
    return redirect(reverse("authors:login"))


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
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        id=id,
    ).first()

    form = AuthorsRecipeForm(data=request.POST or None,
                             files=request.FILES or None,
                             instance=recipe)

    if not recipe:
        raise Http404()

    if form.is_valid():
        recipe = form.save(commit=False)

        # if len(recipe.title) < 5:
        #     messages.error(request, 'Seu título é muito curto.')
        #     return redirect(reverse('authors:dashboard_recipe_edit',
        #                             args=(id,)))

        # if len(recipe.description) < 20:
        #     messages.error(
        #         request, 'A sua descrição precisa ter, pelo menos, ' +
        #         '20 caracteres')
        #     return redirect(reverse('authors:dashboard_recipe_edit',
        #                             args=(id,)))

        recipe.author = request.user
        recipe.preparation_stes_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id, )))

    return render(request,
                  'authors/pages/dashboard_recipe.html',
                  context={
                      'form': form,
                  })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorsRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)

        recipe.authors = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(
            request, 'Salvo com sucesso. Aguarde um ' +
            'administrador aprovar a sua receita.')
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(recipe.id, )))

    return render(request,
                  'authors/pages/dashboard_recipe.html',
                  context={
                      'form': form,
                      'form_action': reverse('authors:dashboard_recipe_new')
                  })


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
