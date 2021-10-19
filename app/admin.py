from django.contrib import admin
from .models import Customer
from .models import CurrentGame
from .models import Games
from .models import Gameplayed
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'walletbalance')
admin.site.register(Customer)

class CurrentGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'color')
admin.site.register(CurrentGame,CurrentGameAdmin)


class GamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'starttime', )
admin.site.register(Games,GamesAdmin)

class GamesPlayedAdmin(admin.ModelAdmin):
    list_display = ('user', 'gameid','amount','pandl','status' )
admin.site.register(Gameplayed,GamesPlayedAdmin)