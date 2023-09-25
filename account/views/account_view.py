from os import getenv

import requests
from dotenv import load_dotenv
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.helpers.utils import choose_account_type, choose_currency, parse_error_422
from account.serializers.accounts_serializer import AccountSerializer
from auth_user.serializers.notification_serializer import ErrorSerializer

load_dotenv()

accounts_url = getenv("ACCOUNTS_URL")


@extend_schema(
    tags=["Accounts"],
    responses={"message": "Text"},
    parameters=[
        OpenApiParameter(
            name="Currency",
            description="Currency name",
            type=OpenApiTypes.STR,
            enum=choose_currency(),
            location=OpenApiParameter.QUERY,
        ),
    ],
)
class GetAllPostAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="Offset",
                description="Offset",
                type=int,
                location=OpenApiParameter.QUERY,
                default="0",
            ),
            OpenApiParameter(
                name="Limit",
                description="Limit",
                type=int,
                location=OpenApiParameter.QUERY,
                default="100",
            ),
        ],
    )
    def get(self, request: Request) -> Response:
        data_to_send = {
            "user_uuid": str(self.request.user.uuid),
            "offset": request.query_params.get("Offset"),
            "limit": request.query_params.get("Limit"),
        }

        currency = request.query_params.get("Currency")
        if currency is not None:
            data_to_send["currency"] = str(currency)

        try:
            response = requests.post(f"{accounts_url}/accounts/", json=data_to_send)
            response.raise_for_status()
            data = response.json()

            return Response(data, response.status_code)

        except requests.exceptions.RequestException:
            if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                return parse_error_422(response)

            return Response(
                ErrorSerializer({"error": "Accounts service is not available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="Type",
                description="Account type",
                type=OpenApiTypes.STR,
                enum=choose_account_type(),
                location=OpenApiParameter.QUERY,
                default="-",
            ),
        ]
    )
    def post(self, request: Request) -> Response:
        try:
            new_account_data = {
                "currency": request.query_params.get("Currency"),
                "account_type": request.query_params.get("Type"),
                "user_uuid": str(self.request.user.uuid),
            }
            response = requests.post(f"{accounts_url}/accounts/create", json=new_account_data)
            result = Response(response.json())
            result.status_code = response.status_code

            return result

        except requests.exceptions.RequestException:
            if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                return parse_error_422(response)

            return Response(
                ErrorSerializer({"error": f"{response.reason}"}).data,
                status=response.status_code,
            )


@extend_schema(tags=["Accounts"])
class GetPatchAccount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, account_id: int) -> Response:
        data_to_send = {"user_uuid": str(self.request.user.uuid)}

        try:
            response = requests.get(f"{accounts_url}/accounts/{account_id}/", json=data_to_send)
            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException:
            if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                return parse_error_422(response)

            return Response(
                ErrorSerializer({"error": f"{response.reason}"}).data,
                status=response.status_code,
            )


@extend_schema(tags=["Accounts"], responses=AccountSerializer)
class GetAccountByNumber(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, account_number: str) -> Response:
        data_to_send = {
            "user_uuid": str(self.request.user.uuid),
            "number": account_number,
        }

        try:
            response = requests.post(f"{accounts_url}/accounts/number/", json=data_to_send)

            return Response(response.json(), status=response.status_code)

        except requests.exceptions.RequestException:
            if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                return parse_error_422(response)

            return Response(
                ErrorSerializer({"error": f"{response.reason}"}).data,
                status=response.status_code,
            )
