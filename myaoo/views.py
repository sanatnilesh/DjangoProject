# Create your views here.
# Import necessary classes
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm, InterestForm, LoginForm, NewUserForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
from datetime import date
from django.contrib.auth.forms import UserCreationForm


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration SuccessFull")
            return redirect('myaoo:index')
    else:
        form = UserCreationForm()
    return render(request, 'myaoo/register_user.html', {'form': form, })


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    msg = 'Your last login was more than an hour ago !!!!!!!!!!'
    if request.session.get('last_login'):
        msg = "last login was " + request.session['last_login'] + "ago !!!!!!!!!!!!!"
    return render(request, 'myaoo/index.html', {'cat_list': cat_list})


def about(request):
    visits = request.COOKIES.get('about_visits')
    if visits:
        response = render(request, 'myaoo/about.html', {'about_visits': visits})
        about_visits = int(visits) + 1
        response.set_cookie('about_visits', about_visits, expires=100)
    else:
        response = render(request, 'myaoo/about.html', {'about_visits': 1})
        response.set_cookie('about_visits', 1, expires=300, )

    return response


@login_required
def detail(request, cat_no):
    response = HttpResponse()
    categories = Category.objects.filter(id=cat_no).values()
    if not categories:
        response.write(get_object_or_404(categories))
        return response
    products = Product.objects.filter(category=cat_no)
    return render(request, 'myaoo/detail.html', {'cat_name': categories[0].get('warehouse'), 'products': products})


@login_required
def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myaoo/products.html', {'prodlist': prodlist})


@login_required
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST, initial={'status_date': date.today(), 'order_status': 'Order Placed'})
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.product.stock = int(order.product.stock) - 1
                product = Product.objects.get(pk=order.product.id)
                product.stock = product.stock - order.num_units
                product.save()
                order.save()
                msg = 'Your order has been placed successfully'
            else:
                msg = 'We do not have sufficient sock to fill your order.'
            return render(request, 'myaoo/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
    return render(request, 'myaoo/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


@login_required
def productdetail(request, prod_id):
    prod = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == 'Yes':
                prod.interested = prod.interested + 1
                print(prod.id)
                prod.save()
                return redirect('/myaoo/')
            else:
                return redirect('/myaoo/')
    else:
        form = InterestForm()
    return render(request, 'myaoo/productdetail.html', {'form': form, 'prod': prod})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                current_time = datetime.datetime.now()
                request.session['last_login'] = str(current_time)
                request.session.set_expiry(6)
                return HttpResponseRedirect(reverse('myaoo:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myaoo/login.html', {'LoginForm': LoginForm})


@login_required
def user_logout(request):
    del request.session['last_login']
    logout(request)
    return HttpResponseRedirect(reverse('myaoo:index'))


@login_required
def myorders(request, user_id):
    print("redirect")
    if not request.user.is_authenticated:
        redirect('myaoo:user_login')
    try:
        if request.user.is_authenticated:
            user_id = request.user.id
            user_db = Client.objects.get(id=user_id)
            try:
                if_exists = Client.objects.get(username=user_db)
                if user_db:
                    name = list(Order.objects.filter(client=user_db))
                else:
                    msg = 'There are no available orders!'
                    return render(request, 'myaoo/order_response.html', {'msg': msg})
            except:
                msg = 'You are not a registered client!'
                return render(request, 'myaoo/order_response.html', {'msg': msg})

            return render(request, 'myaoo/myorders.html', {'order_list': name})
        else:
            return redirect('myaoo:user_login')
    except:
        return render(request, 'myaoo/generic_response.html', {'response': 'You are not a registered client!!'})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="myaoo/register.html", context={"register_form": form})
