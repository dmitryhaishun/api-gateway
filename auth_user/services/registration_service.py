from datetime import timedelta

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from app.celery.tasks import send_confirm_to_email
from app.settings import redis_client_check_otp as redis_check_otp
from app.settings import redis_client_confirm_otp as redis_confirm_email
from auth_user.serializers.notification_serializer import EmailErrorSerializer, MessageSerializer, OtpErrorSerializer
from auth_user.utils import random_otp


def process_registration_data(email: str, password: str) -> Response:
    if email and not password:
        otp_code = random_otp()

        email_subject = "Confirm your email"
        email_message = (
            "To set up your Pretty Bank account, we need to make sure this email address is yours.\n\n"
            f"To verify your email, please use this confirmation code: {otp_code}\n\n"
            "If you didn't request the code, you can safely ignore this email.\n\n"
            "Kind regards,\n"
            "Pretty Bank"
        )

        send_confirm_to_email.delay(email_subject, email_message, email)

        redis_check_otp.set(email, str(otp_code))
        redis_check_otp.expire(email, timedelta(minutes=15))

        return Response(MessageSerializer({"message": "Otp send, check your email"}).data, status=status.HTTP_200_OK)

    return Response(MessageSerializer({"message": "Ok"}).data, status=status.HTTP_200_OK)


def activate_user(email: str, otp_code: str) -> Response:
    if not email:
        return Response(
            EmailErrorSerializer({"email": "Email required field in this step of registration"}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    otp_from_redis = redis_check_otp.get(email)

    cache_key = f"otp_attempts_{email}"
    attempts = cache.get(cache_key, default=0)

    attempts += 1
    cache.set(cache_key, attempts)

    if not otp_from_redis:
        return Response(
            OtpErrorSerializer({"otp_code": ["Otp code expired. Please try again or request a new code."]}).data,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if otp_code != otp_from_redis.decode():
        if attempts <= 3:
            return Response(
                OtpErrorSerializer(
                    {"otp_code": ["Invalid verification code. Please try again or request a new code"]}
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            OtpErrorSerializer(
                {
                    "otp_code": [
                        "Please try again or request a new code. You have only 3 attempts to write" " correct OTP code"
                    ]
                }
            ).data,
            status=status.HTTP_400_BAD_REQUEST,
        )
    if otp_code == otp_from_redis.decode():
        if attempts <= 3:
            redis_confirm_email.set(email, email)
            redis_confirm_email.expire(email, timedelta(minutes=15))
            return Response(
                MessageSerializer({"message": "User activated successfully."}).data,
                status=status.HTTP_200_OK,
            )
        return Response(
            OtpErrorSerializer(
                {
                    "otp_code": [
                        "Please try again or request a new code. You have only" " 3 attempts to write correct OTP code"
                    ]
                }
            ).data,
            status=status.HTTP_400_BAD_REQUEST,
        )
