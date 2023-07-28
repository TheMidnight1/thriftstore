from django.shortcuts import render, redirect
from products.views import delete_product
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from products.models import Product,Comment,Review
from useraccount.models import User
from categories.models import Category,Condition
from payment.models import UserPayment
from django.core.paginator import Paginator

products = Product.objects.all()
users  = User.objects.all()
categories  = Category.objects.all()
conditions  = Condition.objects.all()
payments = UserPayment.objects.all()

class admin_login(LoginView):
    form_class = LoginForm
    template_name = "admin_login.html"


def admin_homepage(request):

    print(payments)
    
    paginator = Paginator(users,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("Page:", page_number)
    print("Page Object:", page_obj)

    
    
    context = {
        'products':products.count(),
        'users':users,
        'categories':categories.count(),
        'conditions':conditions.count(),
        'page_obj': page_obj
        }
    return render(request, "admin_homepage.html",context)

def manage_products(request):
    search_query = request.GET.get('search')
    filtered_products = products

    if search_query:
        filtered_products = products.filter(name__icontains=search_query)

    context = {'products': filtered_products}
    return render(request, 'products.html', context)

# def delete_product(request):

def manage_condition(request):
    context = {'conditions': conditions}
    print(conditions)
    return render(request, 'condition.html', context)


def manage_users(request):
    context = {'users': users}
    return render(request, 'users.html', context)

def manage_categories(request):
    context = {'categories': categories}
    return render(request, 'categories.html', context)
