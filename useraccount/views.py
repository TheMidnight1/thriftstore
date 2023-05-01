from .models import User
from .forms import UserForm
from .forms import LoginForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# def RegisterView(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(
#                 "login"
#             )  # Redirect to the homepage after successful registration
#     else:
#         form = UserForm()
#     context = {"form": form}
#     return render(request, "register.html", context)


class MyRegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = "register.html"
    success_url = reverse_lazy("useraccount:login")


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:  # Check if user is logged in
            # Redirect to homepage or any other URL
            return redirect("products:homepage")
        else:
            return super().dispatch(request, *args, **kwargs)


class Logout(LogoutView):
    next_page = reverse_lazy("useraccount:login")
