from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

#For the group model to section assign specific functionalities to users based on their groups 

from django.contrib.auth.models import Group

from .models import *
from .forms import *

#Import the filters file
from .filters import OrderFilter

#To get flash messages for the register form authentication
from django.contrib import messages

#For the authentication decorators as designed in decorators.py 
from .decorators import unauthenticated_user, allowed_users , admin_only

# Create your views here.

@login_required(login_url = 'login')
@admin_only
def IndexPage(request):
    
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    if orders.filter(status = 'Pending').count() != None:
        orders_pending = 0
    orders_pending = orders.filter(status = 'Pending').count()
    customers = Customer.objects.all()

    context = {
        'orders' : orders,
        'customers' : customers,
        'total_orders' : total_orders,
        'orders_delivered' : orders_delivered,
        'orders_pending' : orders_pending,
    }
    return render(request, 'index.html', context)


#Login page view for with user permissions and authentication
@unauthenticated_user
def LoginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else: 
            messages.info(request, 'Email or Password is Incorrect ! ')
    context = {}
    return render(request, 'login.html', context)


#Logout user view with user redirect to login when logged out

def LogoutUser(request):
    logout(request)
    return redirect('login')


#Register page view  

@unauthenticated_user
def RegisterPage(request):


    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # #To get the group using the Group model imported from django.cotrib.auth.models to assign users to their specific groups i.e customer
            # group = Group.objects.get(name = "customer")
            # #Adding the user to the customer group
            # user.groups.add(group)

            # #To Create the customer in the customer model once the user is registered referecing the Customer model 

            # Customer.objects.create(
            #     user = user, name = user.username
            # )

            #Flash messages for action alerts 
            messages.success(request, 'Account was created for '+ username+ ' Successfully')
            return  redirect('login')
    context = {
        'form' : form
    }
    return render(request, 'register.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def ProductsPage(request):
    products = Product.objects.all().order_by('-date_created')

    context = {
        'products' : products
    }
    return render(request, 'products.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def CustomerPage(request, pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()

    filter_customers = OrderFilter(request.GET, queryset = orders)
    orders = filter_customers.qs
    order_count = orders.count()

    context = {
        'customer' : customer,
        'orders' : orders,
        'order_count' : order_count,
        'filter_customers': filter_customers,
    }
    return render(request, 'customer.html', context)


@login_required(login_url = 'login')
def OrderPage(request):

    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form' : form
        }

    return render(request, 'order.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def UpdatePage(request, pk):

    order = Order.objects.get(id = pk)
    form = OrderForm(instance = order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form,
        
    }

    return render(request, 'order.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def DeletePage(request, pk):

    order = Order.objects.get(id = pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'order' : order
    }

    return render(request, 'delete.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['admin'])
def PlaceOrder(request, pk):

    customer = Customer.objects.get(id = pk)
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra = 6)
    # form = OrderForm(initial = {'customer' : customer})

    formset = OrderFormSet(queryset = Order.objects.none(), instance = customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}

    return render(request, 'place_order.html', context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['customer'])
def UserPage(request):

    #access the orders for each specific customer using the one to one field relationship between customer and user and OneToMany Relationship between customer and order
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status = 'Pending').count()
    print('ORDERS :', orders)
    context = {
        'orders' : orders,
        'total_orders' : total_orders,
        'orders_delivered' : orders_delivered,
        'orders_pending' : orders_pending,
    }
    return render(request, 'userpage.html', context)

@login_required(login_url = 'login')

def ProfilePage(request):

    #To add the form fields for updating customer information

    customer = request.user.customer 
    #Set the instance of the customer form to be that of the currently logged in user/customer
    form = CustomerForm(instance = customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid():
            form.save()
    context = {
        'form' : form,
    }
    return render(request, 'profile_page.html', context)
   


        