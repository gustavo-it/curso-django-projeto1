import os

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


@login_required(login_url="authors:login", redirect_field_name="next")
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    messages.success(request, 'Você acabou de fazer logout.')
    logout(request)
    return redirect(reverse("authors:login"))
