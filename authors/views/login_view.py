import os

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from ..forms import LoginForm

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


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
