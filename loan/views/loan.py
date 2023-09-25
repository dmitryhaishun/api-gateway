import os
import requests
from dotenv import load_dotenv
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serializers.notification_serializer import ErrorSerializer
from loan.helpers.utils import choose_loan_type
from loan.serializers.serializers import LoanCreateIncomingSerializer

load_dotenv()
loans_url = os.getenv("LOANS_URL")


@extend_schema(tags=["Loans"])
class CreateNewLoanView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=LoanCreateIncomingSerializer)
    def post(self, request) -> Response:
        try:
            request.data["user_uuid"] = str(request.user.uuid)
            response = requests.post(f"{loans_url}/loans/create", json=request.data)
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Loans service is not available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(tags=["Loans"])
class GetAllLoansWithFilterView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="loan_type",
                description="Choose a loan type",
                type=OpenApiTypes.STR,
                enum=choose_loan_type(),
                location=OpenApiParameter.QUERY,
                default="loans",
            ),
            OpenApiParameter(
                name="limit",
                description="Choose the Limit",
                type=int,
                location=OpenApiParameter.QUERY,
                default="100",
            ),
            OpenApiParameter(
                name="offset",
                description="Choose the offset",
                type=int,
                location=OpenApiParameter.QUERY,
                default="0",
            ),
        ],
    )
    def get(self, request) -> list | Response:
        data = {
            "user_uuid": str(request.user.uuid),
            "loan_type": request.query_params.get("loan_type"),
            "offset": request.query_params.get("offset"),
            "limit": request.query_params.get("limit"),
        }
        try:
            response = requests.post(f"{loans_url}/loans/", json=data)
            response.raise_for_status()
            data = response.json()
            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Loans service is not available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(tags=["Loans"])
class GetLoansByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, loan_id) -> Response:
        data = {
            "user_uuid": str(request.user.uuid),
            "loan_id": loan_id,
        }
        try:
            response = requests.post(f"{loans_url}/loans/{loan_id}/", json=data)
            data = response.json()
            return Response(data, status=response.status_code)
        except requests.exceptions.RequestException:
            return Response(
                ErrorSerializer({"error": "Loans service is not available"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
