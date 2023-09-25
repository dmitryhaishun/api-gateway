import os

import requests
from dotenv import load_dotenv
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serializers.notification_serializer import ErrorSerializer

load_dotenv()
loans_url = os.getenv("LOANS_URL")


@extend_schema(
    tags=["Loan Products"],
)
class GetLoanProductsView(APIView):
    def get(self, request) -> list | Response:
        try:
            response = requests.get(f"{loans_url}/products/")
            data = response.json()
            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Loan service isn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    tags=["Loan Products"],
)
class GetLoanProductByIdView(APIView):
    def get(self, request, loan_product_id: int) -> list | Response:
        try:
            response = requests.get(f"{loans_url}/products/{loan_product_id}/")
            data = response.json()
            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Loan service isn't available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
