from django.urls import path

from card.views.card_products_view import GetCardProducts
from card.views.card_view import GetAllCardsView, GetCardView, CardLimitsView

urlpatterns = [
    path('', GetAllCardsView.as_view(), name='get_cards'),
    path('<int:id>/', GetCardView.as_view(), name='crud_card'),
    path("products/", GetCardProducts.as_view(), name="get_card_products"),
    path("limits/<int:id>/", CardLimitsView.as_view(), name="card_limits"),
]
