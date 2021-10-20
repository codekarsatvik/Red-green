# from django.shortcuts import render
from os import O_RDWR
import django
import datetime

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
from .models import Customer,CurrentGame,Games,Gameplayed
import razorpay
from django.db.models import Sum
client = razorpay.Client(auth=("rzp_test_Kkdle5kEEV51Jj", "xhRhgMgHwr0M699bCYoQZFy0"))

# Create your views here.

def home(request):
    if request.user.is_authenticated:
       
        
        customer=Customer.objects.filter(user=request.user).first()
        games = Games.objects.all()
        currentgame = Games.objects.first()
        # print(currentgame.starttime,datetime.timedelta(minutes = 5,seconds = 0))
        if Games.objects.count() == 1 :
            Games(starttime = datetime.datetime.now() + datetime.timedelta(minutes = 5) ).save()
        
        return render(request, 'home.html',{'customer':customer,'games' :games,'currentgame' :currentgame})
       
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



def submitgame(request):
    color = request.POST.get('color')
    amount = request.POST.get('amount')
    gameid = request.POST.get('gameid')
    customer=Customer.objects.filter(user=request.user).first()
    if int(amount) > customer.walletbalance :
        messages.warning(request,'Your Bid amount is more than your wallet balance,place another bid of lower amount')
        return redirect('/')
    if amount != "0" :
        
        
       
        game = CurrentGame(user =request.user, color = color, amount = amount)
        game.save()
        customer = Customer.objects.filter(user=request.user).first()
        customer.walletbalance = customer.walletbalance - int(amount)
        customer.save()
         
        #  Gameplayed
        Gameplayed(user=request.user, amount = amount,gameid = gameid).save()
        messages.success(request,'Your Bid amount is placed,You will get your result soon')
        return redirect('/')




    return redirect('/')


def winnerlogic(request,gameid):
    # winning logic
        

        amountred = 0
        amtred = CurrentGame.objects.filter(color = "red").aggregate(Sum('amount'))
        if amtred['amount__sum'] != None:
            amountred = amtred['amount__sum']

        amountgreen = 0
        amtgreen = CurrentGame.objects.filter(color = "green").aggregate(Sum('amount'))
        if amtgreen['amount__sum'] != None:
            amountgreen = amtgreen['amount__sum']
        
        isWinner = "Not Played"

        # 
        if CurrentGame.objects.filter(user = request.user).count() >0 :
            isWinner = "You Loose"
        if(amountred > amountgreen):
            winners = CurrentGame.objects.filter(color = "green")
            

        else :
            winners = CurrentGame.objects.filter(color = "red")
        for winner in winners:
                if(winner.user == request.user):
                    isWinner = "You Won"
                customer=Customer.objects.filter(user=winner.user).first()
                # 
                gameplayed = Gameplayed.objects.filter(user=request.user).filter(gameid = gameid).first()
                gameplayed.status = "Won"
                gameplayed.pandl = (0.8)*winner.amount
                gameplayed.save()
                print(customer)
                Customer(id =  customer.id,user= winner.user,walletbalance = winner.amount*(1.8) + customer.walletbalance).save()   

        
       
        return  JsonResponse({'isWinner' : isWinner },safe= False)

def mygames(request):
    mygames = reversed(Gameplayed.objects.filter(user = request.user))
    return render(request,'mygames.html',{'mygames':mygames})


def creategame(request,gameid):
        CurrentGame.objects.all().delete()
        Games.objects.get(id = gameid).delete()
        # currentgame = Games.objects.first()
        Games(starttime = datetime.datetime.now() + datetime.timedelta(minutes = 5) ).save()
        return redirect('/')