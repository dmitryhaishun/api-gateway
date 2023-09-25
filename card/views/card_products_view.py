import requests
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serializers.notification_serializer import ErrorSerializer
from card.views.card_view import cards_url


@extend_schema(
    tags=["Cards"],
)
class GetCardProducts(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        try:
            response = requests.get(f"{cards_url}/products")
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card products service isn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
