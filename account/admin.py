from django.contrib import admin

# Register your models here.
from account.models import MyAccount, Account



class MyAccountAdmin(admin.ModelAdmin):
   
    list_display  = ("id", "name","isactivate")


class AccountAdmin(admin.ModelAdmin):
     fields = ("name",)
     list_display  = ("id", "fake_id","name","create_time")


admin.site.register(MyAccount, MyAccountAdmin)
admin.site.register(Account, AccountAdmin)