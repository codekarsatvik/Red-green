# from django.shortcuts import render
from os import O_RDWR
import django
from redgreen.settings import RAZORPAY_API_KEY
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import  CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import Customer
import razorpay
client = razorpay.Client(auth=("rzp_test_Kkdle5kEEV51Jj", "xhRhgMgHwr0M699bCYoQZFy0"))

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        customer=Customer.objects.filter(user=request.user).first()
        return render(request, 'home.html',{'customer':customer})
       
    return render(request, 'home.html')

def wallet(request):
    if request.user.is_authenticated:
        customer=Customer.objects.filter(user=request.user).first()
    return render(request, 'wallet.html',{'customer':customer})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! You are registered successfully')
            # form.save()
            user = form.save( commit= False)
            user.save()
            # usr=form.cleaned_data['username']
            reg=Customer(user=user,walletbalance=100)
            reg.save()
        return render(request,'customerregistration.html',{'form':form})

@login_required
def wallet(request):
    
    customer=Customer.objects.filter(user=request.user).first()
    # total_amount=0
    # print(total_amount)
    # if request.method=='POST':
    #     total_amount=int(request.POST.get('add'))
    #     print(total_amount)
    #     order_amount = total_amount*100
    #     order_currency = 'INR'
    #     payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
    #     payment_order_id=payment_order['id']
    #     return render(request, 'wallet.html',{'totalamount':total_amount,'order_id':payment_order_id,'api_key':RAZORPAY_API_KEY,'amount':total_amount})
    
    
    

    return render(request, 'wallet.html',{'customer':customer})

# @login_required
# def wallet(request):
    
#     customer=Customer.objects.filter(user=request.user).first()
#     total_amount=request.POST.get('add')
#     print(total_amount)
#     order_amount = total_amount*100
#     order_currency = 'INR'
#     payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
#     payment_order_id=payment_order['id']
    

#     return render(request, 'wallet.html',{'customer':customer,'totalamount':total_amount,'order_id':payment_order_id,'api_key':RAZORPAY_API_KEY,'amount':total_amount})

@login_required
def Addamount(request):
    # if request.user.is_authenticated:
    user=request.user

    total_amount = int(request.POST.get('add'))
    print(total_amount)
    order_amount = total_amount*100
    order_currency = 'INR'
    payment_order=client.order.create(dict(amount=order_amount, currency=order_currency,payment_capture=1 ))
    payment_order_id=payment_order['id']
    return render(request, 'confirmamount.html',{'totalamount':total_amount,'order_id':payment_order_id,'api_key':RAZORPAY_API_KEY,'amount':total_amount})

# @login_required
# class wallet(View):
    
#     def get(self,request):
#         customer=Customer.objects.filter(user=request.user).first()
#         return render(request, 'wallet.html',{'customer':customer})
    
#     def post(self,request):
#         form=CustomerRegistrationForm(request.POST)
#         # if form.is_valid():
#         #     messages.success(request,'Congratulations!! You are registered successfully')
#         #     form.save()
#         return render(request,'app/customerregistration.html',{'form':form})
#     customer=Customer.objects.filter(user=request.user).first()
#     total_amount=request.POST.get('add')
#     print(total_amount)
    
    

#     return render(request, 'wallet.html',{'customer':customer})


@login_required
def payment_done(request):
    
    amount = int(request.POST.get('amount'))
    customer=Customer.objects.filter(user=request.user).first()
    
    Customer(id =  customer.id,user= request.user,walletbalance = amount + customer.walletbalance).save()
    print(amount,customer)
    messages.success(request,'Your payment was successful ,Wallet Balnce Updated')
    return  redirect('/wallet')