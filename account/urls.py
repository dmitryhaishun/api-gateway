from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from account.views.example_view import AccountAPI
from .views.account_view import GetAllPostAccountsView, GetPatchAccount, GetAccountByNumber
from .views.atm_view import AtmsView, AtmsCity
from .views.currency_rate_view import CurrencyExchange
from .views.transaction_view import Transactions, FavoriteTransactions, CardTransactions

router = DefaultRouter()
router.register(r'exchange-rates', CurrencyExchange, basename='exchange-rates')
router.register(r'atms', AtmsView, basename='atms')
router.register(r'atms/cities', AtmsCity, basename='atms_cities')

urlpatterns = [
    path("", GetAllPostAccountsView.as_view(), name="accounts-all"),
    path("example", AccountAPI.as_view(), name="account-api"),
    re_path(r'^(?P<account_id>[0-9]+)/', GetPatchAccount.as_view(), name='account-id'),
    re_path(r'number/(?P<account_number>[0-9]{16})/', GetAccountByNumber.as_view(), name='account-number'),
    path(r'transactions/', Transactions.as_view(), name='transactions'),
    path(r'transactions/favorite/', FavoriteTransactions.as_view(), name='favorite_transactions'),
    path(r'card-transactions/', CardTransactions.as_view(), name='card_transactions'),
]

urlpatterns.extend(router.urls)
