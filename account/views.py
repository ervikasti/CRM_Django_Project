from django.shortcuts import render, redirect
from account.models import Product, Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from .forms import OrderForm, CustomerForm, RegisterForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only

# the below import is used to create multiple form one
from django.forms import inlineformset_factory
from django.contrib import messages


# Create your views h.


@unauthenticated_user
def registerPage(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(
                request, 'Account Craeted Successfully of '+username)
            # return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    '''below is the django default decorator '''
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # lets authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username OR Password incorrect')

    return render(request, 'accounts/login.html', {'login': 'Login'})


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    order = Order.objects.all().order_by('-date_created')
    customer = Customer.objects.all()

    total_orders = order.count()
    order_delivered = order.filter(status='Delivered').count()
    order_pending = order.filter(status='Pending').count()

    homeDict = {
        'order': order,
        'customer': customer,
        'total_orders': total_orders,
        'order_delivered': order_delivered,
        'order_pending': order_pending,
    }
    return render(request, 'accounts/dashboard.html', homeDict)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    prodDict = {
        'product': product,
    }
    return render(request, 'accounts/product.html', prodDict)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    total_order = customer.order_set.all().count()
    orders = customer.order_set.all()
    myFilters = OrderFilter(request.GET, queryset=orders)
    orders = myFilters.qs

    custDict = {
        'customer': customer,
        'total_order': total_order,
        'orders': orders,
        'myFilters': myFilters,
    }
    return render(request, 'accounts/customer.html', custDict)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'customer'), extra=5)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
       # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    creOrd = {'formset': formset}
    return render(request, 'accounts/order_form.html', creOrd)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    creOrd = {'formset': form,'order':order}
    return render(request, 'accounts/update_order.html', creOrd)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    delOrd = {'item': order}
    return render(request, 'accounts/delete_form.html', delOrd)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    customer = CustomerForm()
    if request.method == "POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
            return redirect('/')

    context = {'customer': customer}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    name = request.user.customer.name
    customer = Customer.objects.get(name=name)
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
   # print('ORDERS',orders)
    context={'order':orders,
    'total_orders':total_orders,
    'order_delivered':order_delivered,
    'order_pending':order_pending,
    'customer':customer,
    }
    return render(request, 'accounts/user_page.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

