from .models import User
from .forms import LoginForm
from products.models import Product
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView


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


class UserProfile(LoginRequiredMixin, ListView):
    model = Product
    template_name = "user_profile.html"
    context_object_name = "products"

    def get_queryset(self):
        # Return only products posted by the current user
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class Logout(LogoutView):
    next_page = reverse_lazy("useraccount:login")


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EditProfileForm
    template_name = "edit_profile.html"
    success_url = reverse_lazy("useraccount:edit_profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["password_form"] = ChangePasswordForm(
                self.request.user, self.request.POST
            )
        else:
            context["password_form"] = ChangePasswordForm(self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        password_form = context["password_form"]
        if password_form.is_valid():
            password_form.save()
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    context_object_name = "form"
    success_url = reverse_lazy("useraccount:edit_profile")
