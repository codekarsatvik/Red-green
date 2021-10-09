# from django.contrib import admin
# from django.urls import path,include
# from app import views ;
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.home ,name = "home"),
    path('wallet/',views.wallet, name = "wallet"),
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('addamount/',views.Addamount,name='addamount'),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    

]
