from os import getenv

import requests
from drf_spectacular.utils import extend_schema
from requests import RequestException
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.helpers.utils import get_rates, parse_error_422
from account.serializers.transactions_serializer import (
    CardTransactionRequestSerializer,
    SuccessSerializer,
    TransactionRequestSerializer,
)
from auth_user.serializers.notification_serializer import ErrorSerializer
from card.serializers.serializers import MessageSerializer

cards_url = getenv("CARDS_URL")
accounts_url = getenv("ACCOUNTS_URL")


@extend_schema(
    tags=["Transactions"],
    request=TransactionRequestSerializer,
    responses={
        status.HTTP_201_CREATED: SuccessSerializer,
        status.HTTP_404_NOT_FOUND: ErrorSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer,
    },
)
class Transactions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            response = requests.get(f"{accounts_url}/transactions/get_transactions/")
            data = response.json()

            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card service doesn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request: Request) -> Response:
        serializer = TransactionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_to_send = {
            "write_off_account": request.data["write_off_account"],
            "crediting_account": request.data["crediting_account"],
            "user_uuid": str(self.request.user.uuid),
            "transaction_sum": request.data["transaction_sum"],
            "is_favourite": request.data["save_transaction"],
            "transaction_type": request.data["transaction_type"],
            "transaction_title": request.data["transaction_title"],
            "rates": get_rates(),
        }

        try:
            response = requests.post(f"{accounts_url}/transactions/", json=data_to_send)
            response.raise_for_status()

        except ConnectionError:
            return Response(ErrorSerializer({"error": "Connection error"}).data, status=status.HTTP_404_NOT_FOUND)

        except RequestException:
            if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                return parse_error_422(response)

            return Response(
                ErrorSerializer({"error": f"{response.json().get('detail', 'Unknown error')}"}).data,
                status=response.status_code,
            )

        return Response(response.json(), status=response.status_code)


@extend_schema(
    tags=["Transactions"],
    request=TransactionRequestSerializer,
    responses={
        status.HTTP_201_CREATED: SuccessSerializer,
        status.HTTP_404_NOT_FOUND: ErrorSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer,
    },
)
class FavoriteTransactions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            response = requests.get(f"{accounts_url}/transactions/get_transactions/favorite/")
            data = response.json()

            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card service doesn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    tags=["Transactions"],
    request=CardTransactionRequestSerializer,
    responses={
        status.HTTP_201_CREATED: SuccessSerializer,
        status.HTTP_404_NOT_FOUND: ErrorSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: ErrorSerializer,
    },
)
class CardTransactions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            uuid = {"user_uuid": str(self.request.user.uuid)}
            serializer = CardTransactionRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            card_response = requests.post(f"{cards_url}/cards/get_cards/", json=uuid)

            account_numbers = {"write_off_account": None, "crediting_account": None}

            found_write_off_card = False
            found_crediting_card = False
            for card in card_response.json():
                if card["number"] == request.data["write_off_card"]:
                    account_numbers["write_off_account"] = card["account_number"]
                    found_write_off_card = True
                if card["number"] == request.data["crediting_card"]:
                    account_numbers["crediting_account"] = card["account_number"]
                    found_crediting_card = True

            if not found_write_off_card:
                return Response(
                    MessageSerializer({"message": "Write off card not found"}).data, status=status.HTTP_404_NOT_FOUND
                )
            if not found_crediting_card:
                return Response(
                    MessageSerializer({"message": "Crediting card not found"}).data, status=status.HTTP_404_NOT_FOUND
                )

            data_to_send = {
                "write_off_account": account_numbers["write_off_account"],
                "crediting_account": account_numbers["crediting_account"],
                "user_uuid": uuid["user_uuid"],
                "transaction_sum": request.data["transaction_sum"],
                "is_favourite": request.data["save_transaction"],
                "transaction_type": request.data["transaction_type"],
                "rates": get_rates(),
            }

            if request.data.get("transaction_title"):
                data_to_send = data_to_send | {"transaction_title": request.data["transaction_title"]}

                response = requests.post(f"{accounts_url}/transactions/", json=data_to_send)
                return Response(response.json(), status=response.status_code)

            response = requests.post(f"{accounts_url}/transactions/", json=data_to_send)
            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            error_message = f"Error while requesting cards: {str(e)}"

            return Response(
                ErrorSerializer({"error": error_message}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
