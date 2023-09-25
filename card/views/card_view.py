import os

import requests
from dotenv import load_dotenv
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serializers.notification_serializer import ErrorSerializer
from card.helpers.enums import CardStatus
from card.helpers.utils import choose_branch, choose_currency, choose_payment_system, choose_product, get_account_number
from card.serializers.card_serializer import AllCardSerializer, CardLimitsSerializer, CardPatchStatusSerializer
from card.serializers.serializers import MessageSerializer

load_dotenv()

cards_url = os.getenv("CARDS_URL")
accounts_url = os.getenv("ACCOUNTS_URL")


@extend_schema(tags=["Cards"])
class GetAllCardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        data_to_send = {"user_uuid": str(self.request.user.uuid)}
        try:
            card_response = requests.post(f"{cards_url}/cards/get_cards/", json=data_to_send)
            account_response = requests.post(f"{accounts_url}/accounts/", json=data_to_send)
            card_response.raise_for_status()
            account_response.raise_for_status()
            card_data = card_response.json()
            account_data = account_response.json()
            result = []
            for card in card_data:
                card_account_number = card["account_number"]
                matching_account = next((acc for acc in account_data if acc["number"] == card_account_number), None)

                card["currency"] = matching_account["currency"] if matching_account else None
                card["amount"] = matching_account["amount"] if matching_account else None
                result.append(card)

            return Response(card_data, card_response.status_code)

        except requests.exceptions.RequestException as e:
            error_message = f"Error while requesting cards: {str(e)}"

            return Response(
                ErrorSerializer({"error": error_message}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        responses={"message": "Text"},
        parameters=[
            OpenApiParameter(
                name="Currency",
                description="Currency name",
                type=OpenApiTypes.STR,
                enum=choose_currency(),
                location=OpenApiParameter.QUERY,
                default="-",
            ),
            OpenApiParameter(
                name="Branch",
                description="Branch address",
                type=OpenApiTypes.STR,
                enum=choose_branch(),
                location=OpenApiParameter.QUERY,
                default="-",
            ),
            OpenApiParameter(
                name="Card Product",
                description="Card Product name",
                type=OpenApiTypes.STR,
                enum=choose_product(),
                location=OpenApiParameter.QUERY,
                default="-",
            ),
            OpenApiParameter(
                name="Payment System",
                description="Payment System name",
                type=OpenApiTypes.STR,
                enum=choose_payment_system(),
                location=OpenApiParameter.QUERY,
                default="-",
            ),
            OpenApiParameter(
                name="account_number",  # Add the parameter for account_number
                description="Account number",
                type=OpenApiTypes.STR,
                # enum=choose_account_number(),
                location=OpenApiParameter.QUERY,
                required=False,  # Set to True if account number is required
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        account_number = request.query_params.get("account_number")
        data = {
            "currency": request.query_params.get("Currency"),
            "payment_system": request.query_params.get("Payment System"),
            "card_product_name": request.query_params.get("Card Product"),
            "address": request.query_params.get("Branch"),
            "cardholder_name": f"{self.request.user.first_name} {self.request.user.last_name}",
            "user_uuid": str(self.request.user.uuid),
        }
        try:
            if account_number:
                if not account_number.isdigit():
                    return Response(
                        data={"message": "Account number can only contain numbers"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                uuid = {
                    "user_uuid": str(self.request.user.uuid),
                }
                response = requests.post(f"{accounts_url}/accounts/", json=uuid)
                account_data = response.json()
                number_list = [number["number"] for number in account_data]

                if account_number not in number_list:
                    return Response(
                        data={"message": "Account number not found"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                new_card_data = data | {
                    "account_number": account_number,
                }

                response = requests.post(f"{cards_url}/cards", json=new_card_data)
                result = Response(response.json())
                result.status_code = response.status_code

                return result

            account_number = get_account_number()
            new_card_data = data | {
                "account_number": account_number,
            }

            response = requests.post(f"{cards_url}/cards", json=new_card_data)
            result = Response(response.json())
            result.status_code = response.status_code

            return result

        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card service doesn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(tags=["Cards"])
class GetCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id: int) -> Response:
        uuid = str(self.request.user.uuid)
        data_to_send = {"user_uuid": str(self.request.user.uuid)}
        try:
            card_response = requests.get(f"{cards_url}/cards/{id}/")
            card_data = card_response.json()
            account_response = requests.post(f"{accounts_url}/accounts/", json=data_to_send)
            account_data = account_response.json()

            if card_response.status_code == 404:
                return Response(
                    MessageSerializer({"message": "Card not found"}).data,
                    card_response.status_code,
                )

            if uuid != card_data["user_uuid"]:
                return Response(
                    MessageSerializer({"message": "This is not your card"}).data, status=status.HTTP_400_BAD_REQUEST
                )

            for account in account_data:
                if account["number"] == card_data["account_number"]:
                    card_data["currency"] = account["currency"]
                    card_data["amount"] = account["amount"]
                    return Response(card_data, status=card_response.status_code)

                if account["number"] != card_data["account_number"]:
                    card_data["currency"] = None
                    card_data["amount"] = None

            return Response(card_data, status=card_response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card service doesn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(request=CardPatchStatusSerializer)
    def patch(self, request: Request, id: int) -> Response:
        new_card_status = request.data.get("status")
        block_reason = request.data.get("block_reason")

        if not new_card_status:
            return Response(
                ErrorSerializer({"error": "Card new status is required"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_card_status != CardStatus.BLOCKED:
            return Response(
                ErrorSerializer({"error": "Wrong new status"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_card_status == CardStatus.BLOCKED and not block_reason:
            return Response(
                ErrorSerializer({"error": "Block reason is required"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.patch(
                f"{cards_url}/cards/{id}/",
                json={
                    "new_card_status": new_card_status,
                    "block_reason": block_reason,
                    "user_uuid": str(self.request.user.uuid),
                },
            )
            response.raise_for_status()
            serializer = AllCardSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError:
            if response.status_code == 404:
                return Response(
                    MessageSerializer({"message": "Card with this id not found"}).data,
                    status=status.HTTP_404_NOT_FOUND,
                )
            if response.status_code == 400:
                return Response(
                    MessageSerializer({"message": "Invalid new status"}).data,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Card service is not available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(request=CardLimitsSerializer, tags=["Cards"])
class CardLimitsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, id: int) -> Response:
        if not request.data:
            return Response(
                MessageSerializer({"message": "All fields can't be empty"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        uuid = str(self.request.user.uuid)
        cash_withdraw_limit = request.data.get("cash_withdraw_limit")
        card_to_card_limit = request.data.get("card_to_card_limit")
        expenses_limit = request.data.get("expenses_limit")

        if cash_withdraw_limit is not None and float(cash_withdraw_limit) <= 0:
            return Response(
                MessageSerializer({"message": "Must be positive number"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if card_to_card_limit is not None and float(card_to_card_limit) <= 0:
            return Response(
                MessageSerializer({"message": "Must be positive number"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if expenses_limit is not None and float(expenses_limit) <= 0:
            return Response(
                MessageSerializer({"message": "Must be positive number"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            response = requests.patch(
                f"{cards_url}/cards/limits/{id}/",
                json={
                    "user_uuid": uuid,
                    "cash_withdraw_limit": cash_withdraw_limit,
                    "card_to_card_limit": card_to_card_limit,
                    "expenses_limit": expenses_limit,
                },
            )
            # response.raise_for_status()
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return Response(
                    MessageSerializer({"message": "Card not found"}).data,
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException as e:
            error_message = f"Error while requesting cards: {str(e)}"

            return Response(
                ErrorSerializer({"error": error_message}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
