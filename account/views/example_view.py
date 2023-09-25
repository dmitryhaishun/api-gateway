from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers.serializers import AccountSerializer
from app.celery.tasks import task
from kafka_core.enums import KafkaTopic
from kafka_core.producer import send_to_kafka


@extend_schema(
    tags=["Example"],
)
class AccountAPI(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        send_to_kafka(KafkaTopic.USER_REGISTRATION, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        text = request.data.get("text")
        task.delay(text)
        data = {"message": f"dasdadadadasda, accounts! You sent: {text}"}
        serializer = AccountSerializer(data)
        return Response(serializer.data)
