from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Cartitem,Customer,ShippingAddress,Order,OrderItems
from .forms import ShippingAddressForm
from django.conf import settings
from django.urls import reverse
import razorpay

from .models import Products 
def product_list(request):
    s = Products.objects.all()
    return render(request, 'products.html', {'s': s})


def product_details(request,id):
    data = Products.objects.get(id=id)
    return render(request, 'product_details.html', {'data': data})

def signup(request):
    if request.method=='POST':
        fn=UserCreationForm(request.POST)
        if fn.is_valid():
            u = fn.save()
            cus = Customer.objects.create(user=u)
            cus.save()
            print(cus)
            return redirect('/login_view')
    else:
        fn=UserCreationForm()
    return render(request,'signup.html',{'form':fn})

def login_view(request):
    if request.method == "POST":
        fn = AuthenticationForm(request=request, data=request.POST)
        if fn.is_valid():
            uname = fn.cleaned_data["username"]
            upass = fn.cleaned_data["password"]
            u1 = authenticate(username=uname, password=upass)
            if u1 is not None:
                login(request,u1)
                return redirect('/product_list')
    else:
        fn = AuthenticationForm()
    return render(request, 'login_view.html', {'form': fn})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def search_result(request):
    query=request.GET.get("q")
    print(query)
    data = Products.objects.filter(Q(sname__icontains=query)|Q(description__icontains=query))
    context={'data':data,'query':query}
    return render(request,'search.html',context)

def add_to_cart(request,product_id):
    products=Products.objects.get(id=product_id)
    customer=Customer.objects.get(user=request.user)
    existing_cart_items=Cartitem.objects.filter(customer__user=request.user,products=products)
    if len(existing_cart_items)==0:
        cart_item=Cartitem.objects.create(customer=customer,products=products)
    else:
        cart_item=existing_cart_items[0]
    cart_item.quantity=request.POST['quantity']
    cart_item.save()
    return redirect('cart_items')


def collect_cart_details(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    qty_list=[n for n in range(1, 6)]
    all_items_price=0
    for item in cart_items_list:
        item.item_price=item.quantity*item.products.price
        all_items_price=all_items_price + item.item_price
    context={
        'cart':cart_items_list,
        'total_price':all_items_price,
        'qty_list':qty_list
    }
    return context


def cart_items(request):
    context=collect_cart_details(request)
    return render(request,'cart_items.html', context=context)

def remove_from_cart(request,product_id):
    products=Products.objects.get(id=product_id)
    cart_item=Cartitem.objects.get(customer__user=request.user.id,products=products)
    cart_item.delete()
    return redirect('cart_items')

def add_address(request):
    if request.method=='POST':
        form=ShippingAddressForm(request.POST)
        if form.is_valid():
            sd=form.save(commit=False)
            sd.customer=Customer.objects.get(user__id=request.POST['customer'])
            sd.save()
            return redirect("order_review",sa_id=sd.id)
    else:
        form=ShippingAddressForm()
    return render(request,'add_address.html',{'form':form})

def order_review(request,sa_id):
    context=collect_cart_details(request)
    context['sa_id']=ShippingAddress.objects.get(id=sa_id)
    return render(request,'order_review.html',context=context)

def clear_cart_details(request):
    cart_items_list=Cartitem.objects.filter(customer__user=request.user)
    for item in cart_items_list:
        item.delete()

def checkout_order(request, sa_id):
    cart_items_list = collect_cart_details(request)['cart']
    customer = Customer.objects.filter(user=request.user)
    delivery_addr = ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order = Order(customer=customer[0], shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItems.objects.create(
                order=order,
                product=item.products,
                price=item.products.price,
                quantity=item.quantity
            )
        # Empty the cart
        clear_cart_details(request)
        # Save order_id for future use in payment order page
        request.session['order_id'] = order.id
        # redirect for payment
        return redirect(reverse('payment_order'))
    else:
        return redirect(reverse('list_all'))


def payment_order(request):
    order_id = request.session.get('order_id')
    print("process_order Order is -> ", order_id)
    order = get_object_or_404(Order, id=order_id)
    amount = int(order.get_total_cost())
    amount_inr = amount

    context = {
        'order_id': order_id,
        'public_key': settings.RAZOR_KEY_ID,
        'amount': amount_inr,
        'amountorig': amount
    }
    return render(
        request,
        'created.html',
        context=context
    )



client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
def payment_process(request, order_id, amount):
    order = get_object_or_404(Order, id=order_id)
    amount=int(order.get_total_cost()*100)
    if request.method == "POST":
        order.complete = True
        order.save()
        print("Amount ", amount)
        print("Type amount str to int ", amount)
        payment_id = request.POST['razorpay_payment_id']
        print("Payment Id", payment_id)
        order.transaction_id = payment_id
        order.save()
        payment_client_capture = (client.payment.capture(payment_id, amount))
        print("Payment Client capture", payment_client_capture)
        payment_fetch = client.payment.fetch(payment_id)
        status = payment_fetch['status']
        amount_fetch = payment_fetch['amount']
        amount_fetch_inr = amount_fetch
        print("Payment Fetch", payment_fetch['status'])
        context = {
            'amount': amount_fetch_inr,
            'status': status,
            'transaction_id': payment_id
        }
        return render(request, 'done.html', context=context)
