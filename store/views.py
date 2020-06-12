from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
import json
import datetime
from store.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView , DetailView
from store.utils import cookieCart , guestOrder
# Create your views here.


def store(request):
    print(request.user.username)
    if request.user.is_authenticated:
        customer , create = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email)
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        print('cartItems',cartItems)
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']


    products = Product.objects.all()[:8]
    context = {'products': products,'cartItems':cartItems , 'shipping':False}
    return render(request,'store/store.html',context)



def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        print(items)
    else:                                      #We are stroring values in cokies for AnonymousUser
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items':items , 'order' : order,'cartItems':cartItems , 'shipping':False}
    return render(request,'store/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {'items':items , 'order' : order,'cartItems':cartItems , 'shipping':False}
    return render(request,'store/checkout.html',context)



def updateUserOrder(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId :', productId)
    print('action :', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem , created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()


    return JsonResponse("Sending Json data",safe=False)




def processOrder(request):
    print('Data :',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer , order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            pincode = data['shipping']['pincode']
        )

    return JsonResponse("Payment Completed",safe=False)


class SignUp(CreateView):
    form_class = UserRegistrationForm
    template_name = 'store/signup.html'
    success_url = reverse_lazy('login')


class ProductDetailView(DetailView):
    context_object_name = 'product_detail'
    model = Product
    template_name = 'store/product_detail.html'


def myOrder(request,pk):
    try:
        if request.user.is_authenticated:
            customer = request.user.customer
            cur_order = Order.objects.get(customer=customer,complete=False)  #for current order , getting order id
            cur_items = cur_order.orderitem_set.all()                        #for current order id , getting all items of the order id
            cartItems = cur_order.get_cart_item                              # getting cart item count for current order
            print(cartItems)
            '''
            orderItem = []
            order = Order.objects.filter(customer=customer,complete=True)   #getting all order of loginin customer
            for myorder in order:
                item = myorder.orderitem_set.all()                          #getting items for each order
                orderItem.append(item)
            '''
            order = Order.objects.filter(customer=customer,complete=True)
            orderItem = OrderItem.objects.filter(order__in=order)
            print("OrderItem",orderItem[0].product.price)
    except:
        order = 0
        orderItem = 0
        cartItems = cur_order.get_cart_item
    context = {'order':order,'orderItem':orderItem,'cartItems':cartItems}
    return render(request,'store/myOrder.html',context)



def playerProduct(request,name):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        mes = 0
        cris = 0

        if name == 'cristiano':
            cris = Product.objects.filter(name='Cristiano Ronaldo')

        if name == 'messi':
            mes = Product.objects.filter(name='Lionel Messi')


        print('player',cris)
        print('messi',mes)
    else:
        mes = 0
        cris = 0
        if name == 'cristiano':
            cris = Product.objects.filter(name='Cristiano Ronaldo')

        if name == 'messi':
            mes = Product.objects.filter(name='Lionel Messi')


        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    context = {'cris':cris,'cartItems':cartItems , 'shipping':False,'mes':mes}
    return render(request,'store/player.html',context)
