from django.db import models


class CurrencyRate(models.Model):
    currency = models.CharField(max_length=50, blank=False, unique=True)
    currency_name = models.CharField(max_length=50, blank=False)
    buy = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    sell = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    image = models.ImageField(upload_to="media/", blank=False)

    def __str__(self) -> str:
        return self.currency


class ATM(models.Model):
    country = models.CharField(blank=False)
    city = models.CharField(blank=False)
    address = models.CharField(blank=False)
    atm_name = models.CharField(blank=False)
    atm_number = models.CharField(blank=False)

    class Meta:
        ordering = ("country", "city", "address")

    def __str__(self) -> str:
        return self.atm_name
