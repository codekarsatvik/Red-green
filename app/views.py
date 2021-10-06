# from django.shortcuts import render
from os import O_RDWR
import django
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

