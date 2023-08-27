import django.http
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from products.models import Product
from useraccount.models import User
from categories.models import Category,Condition
from payment.models import UserPayment
from django.core.paginator import Paginator

from .forms import ConditionForm,CategoryForm


payments = UserPayment.objects.all()

class admin_login(LoginView):
    form_class = LoginForm
    template_name = "admin_login.html"


def admin_homepage(request):
    conditions  = Condition.objects.all()
    categories  = Category.objects.all()
    products = Product.objects.all()
    users  = User.objects.all()

    
    paginator = Paginator(users,7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products':products.count(),
        'users':users,
        'categories':categories.count(),
        'conditions':conditions.count(),
        'page_obj': page_obj
        }
    return render(request, "admin_homepage.html",context)

def manage_products(request):
    products = Product.objects.all()
    
    search_query = request.GET.get('search')
    filtered_products = products

    if search_query:
        filtered_products = products.filter(name__icontains=search_query)

    context = {'products': filtered_products}
    return render(request, 'products.html', context)


def delete_product(request, pk):
    products  = Product.objects.all()
    product = get_object_or_404(products, pk=pk)
    product.delete()
    return redirect("/products/")

# def delete_product(request):

def manage_condition(request):
    conditions  = Condition.objects.all()
    context = {'conditions': conditions}
    return render(request, 'condition.html', context)

# def delete_condition(request, pk):
#     conditions = get_object_or_404(Condition, pk=pk)

#     conditions.delete()
#     return redirect("thriftAdmin:conditions")


def add_condition(request):    
    if request.method == 'POST':
        form = ConditionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/conditions/')
        else:   
            print(form.errors)
    else:
        form = ConditionForm()

    context = {'form':form}
    return render(request,'add_condition.html',context)

def edit_condition(request,pk):
    condition = get_object_or_404(Condition, pk=pk)
    if request.method == 'POST':
        form = ConditionForm(request.POST, instance=condition)
        if form.is_valid():
            form.save()
            return redirect('/conditions/')
        else:   
            print(form.errors)
    else:
        form = ConditionForm(instance=condition)

    context = {"condition":condition , 'form':form}
    return render(request,'edit_condition.html',context)


def manage_users(request):
    users  = User.objects.all()
    context = {'users': users}
    return render(request, 'users.html', context)

def delete_user(request, pk):
    users  = User.objects.all()
    user = get_object_or_404(users, pk=pk)
    user.delete()
    return redirect("/users/")

def manage_categories(request):
    categories  = Category.objects.all()
    
    context = {'categories': categories}
    return render(request, 'categories.html', context)

def add_category(request):    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categories/')
        else:   
            print(form.errors)
    else:
        form = CategoryForm()

    context = {'form':form}
    return render(request,'add_category.html',context)

def delete_category(request, pk):
    categories  = Category.objects.all()
    category = get_object_or_404(categories, pk=pk)
    category.delete()
    return redirect("/categories/")

def edit_category(request,pk):
    categories  = Category.objects.all()
    
    category = get_object_or_404(categories, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/categories/')
        else:   
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {"category":category , 'form':form}
    return render(request,'edit_category.html',context)