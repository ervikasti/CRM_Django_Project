from django.shortcuts import render,redirect
from account.models import Product,Order,Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from .forms import OrderForm,CustomerForm,RegisterForm
from .filters import OrderFilter

#the below import is used to create multiple form one
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views h.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form  = RegisterForm()
        
        if request.method == "POST":
            form  = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account Craeted Successfully of '+username)
                #return redirect('login')
                
        context ={'form':form}
        return render(request, 'accounts/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =="POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            #lets authenticate
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'username OR Password incorrect')

        return render(request, 'accounts/login.html',{'login':'Login'})

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    order  = Order.objects.all()
    customer =Customer.objects.all()


    total_orders = order.count()
    order_delivered = order.filter(status='Delivered').count()
    order_pending = order.filter(status='Pending').count()


    homeDict = {
        'order': order,
        'customer':customer,
        'total_orders':total_orders,
        'order_delivered':order_delivered,
        'order_pending':order_pending,
    }
    return render(request, 'accounts/dashboard.html', homeDict)

@login_required(login_url='login')
def product(request):
    product = Product.objects.all()
    prodDict = {
        'product': product,
    }
    return render(request, 'accounts/product.html', prodDict)

@login_required(login_url='login')
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    total_order = customer.order_set.all().count()
    orders = customer.order_set.all()
    myFilters = OrderFilter(request.GET,queryset=orders)
    orders = myFilters.qs
    
    custDict = {
        'customer' : customer,
        'total_order': total_order,
        'orders': orders,
        'myFilters':myFilters,
    }
    return render(request, 'accounts/customer.html', custDict)

@login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == "POST":
        formset = OrderFormSet(request.POST,instance=customer)
       # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    creOrd={'formset':formset}
    return render(request, 'accounts/order_form.html', creOrd)

@login_required(login_url='login')
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    creOrd={'form':form}
    return render(request, 'accounts/update_order.html', creOrd)

@login_required(login_url='login')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    delOrd={'item':order}
    return render(request, 'accounts/delete_form.html', delOrd)

@login_required(login_url='login')
def createCustomer(request):
    customer = CustomerForm()
    if request.method=="POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
            return redirect('/')

       
    context = {'customer':customer}
    return render(request, 'accounts/customer_form.html', context)
