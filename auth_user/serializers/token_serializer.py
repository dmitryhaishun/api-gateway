from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User) -> str:
        token = super().get_token(user)
        token["username"] = user.email
        return token

    def validate(self, value) -> dict:
        email = value.get("email")
        error_message = None

        if "@" not in email and "." not in email:
            error_message = "Email wrong format"
        elif "@" not in email:
            error_message = "Email wrong format. Try adding a '@' symbol"
        elif "." not in email[email.index("@") :]:  # noqa
            error_message = "Email wrong format. Try adding a '.' symbol"

        if error_message:
            raise exceptions.ValidationError({"message": error_message})

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.ValidationError({"message": "Email doesn't exist. Please check and try again"})

        try:
            data = super().validate(value)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed({"message": "Wrong password. Please, try again"})
        else:
            return data


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.CharField()
