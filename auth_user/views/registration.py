from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from app.celery.tasks import send_message
from app.settings import redis_client_confirm_otp as redis_confirm_email
from auth_user.serializers.auth_serializer import UserRegistrationRequiredFieldsSerializer, UserRegistrationSerializer
from auth_user.serializers.notification_serializer import EmailErrorSerializer
from auth_user.services.registration_service import activate_user, process_registration_data
from user.models import User


@extend_schema(
    tags=["Registration"],
    request=UserRegistrationSerializer,
)
class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data.get("otp_code")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        if not email and otp_code:
            return Response(
                EmailErrorSerializer({"email": "Email required field in this step of registration"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and otp_code:
            return activate_user(email, otp_code)

        return process_registration_data(email, password)


@extend_schema(
    tags=["Registration"],
    request=UserRegistrationRequiredFieldsSerializer,
)
class FinalRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationRequiredFieldsSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        redis_email = redis_confirm_email.get(email)

        if not redis_email or email != redis_email.decode():
            return Response(
                EmailErrorSerializer({"email": "You should confirm email"}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.save()
        send_message.delay(user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
