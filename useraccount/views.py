from .models import User
from products.models import Product
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import  ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, EditProfileForm, ChangePasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView



class MyRegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = "register.html"
    success_url = reverse_lazy("useraccount:login") 


class MyLoginView(LoginView):
    template_name = "login.html"
    
    def form_valid(self, form):
        # Log the user in using Django's built-in authentication
        response = super().form_valid(form)

        # Redirect the user based on their role (admin or user)
        user = self.request.user
        print(user)
        if user.is_superuser:
            return redirect('thriftAdmin:admin_homepage')
        
        elif user.is_user:
            return redirect('products:homepage')
            
        else:
            return redirect('products:homepage')

        return response

    def get_success_url(self):
        # Override this method to prevent any further redirection by the LoginView
        return self.request.path

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
        
        # Handle image upload
        if "image" in self.request.FILES:
            image_file = self.request.FILES["image"]
            self.object.image = image_file
            self.object.save()
            
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    context_object_name = "form"
    success_url = reverse_lazy("useraccount:edit_profile")

User = get_user_model()
        
        
