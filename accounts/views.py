from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .form import OrderForm
from .models import *


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status = 'pending').count()
    context = {
        'orders' : orders,
        'customers' : customers,
        'total_orders': total_orders,
        'delivered':delivered,
        'total_customers':total_customers,
        'pending': pending

    }
    return render(request, 'home.html', context)


def products(request):
    product = Products.objects.all()

    return render(request, 'products.html', {'list':product})


def customer(request, pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'orders_count': orders_count
    }
    return render(request, 'customer.html', context)


def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product', 'status'),extra=5)
    customer = Customer.objects.get(id = pk)
    # form = OrderForm(initial = {'customer':customer})
    formset = OrderFormSet(queryset =Order.objects.none(),instance =customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance =customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'order_form.html',context)


def updateOrder(request,pk):
    order = Order.objects.get(id =pk)

    form = OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context ={'item':order}
    return  render(request, 'delete.html', context)