from django.contrib import admin

from account.models import ATM, CurrencyRate


class CurrencyRateAdmin(admin.ModelAdmin):
    search_fields = ("currency", "currency_name", "buy", "sell")
    list_display = ("id", "currency", "currency_name", "buy", "sell", "image")


class ATMAdmin(admin.ModelAdmin):
    search_fields = ("country", "city", "address", "atm_name", "atm_number")
    list_display = ("id", "country", "city", "address", "atm_name", "atm_number")


admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(ATM, ATMAdmin)
