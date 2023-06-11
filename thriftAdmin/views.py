from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.views import LoginView


class admin_login(LoginView):
    form_class = LoginForm
    template_name = "admin_login.html"


def admin_homepage(request):
    return render(request, "admin_homepage.html")
