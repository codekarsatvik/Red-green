from django.contrib import admin
from .models import Customer
from .models import CurrentGame
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'walletbalance')
admin.site.register(Customer)

class CurrentGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'color')
admin.site.register(CurrentGame,CurrentGameAdmin)