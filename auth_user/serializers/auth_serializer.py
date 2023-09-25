from string import ascii_lowercase, ascii_uppercase

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    otp_code = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def validate(self, value: dict) -> dict:
        password = value.get("password")
        password2 = value.get("password2")

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return value

    def validate_first_name(self, value: str) -> str:
        if value and all(char in "- '" for char in value):
            raise serializers.ValidationError("Invalid first name")

        return value

    def validate_last_name(self, value: str) -> str:
        if value and all(char in "- '" for char in value):
            raise serializers.ValidationError("Invalid last name")

        return value

    def validate_email(self, value: str) -> str:
        lowercase = [letter for letter in ascii_lowercase]
        uppercase = [letter for letter in ascii_uppercase]
        numbers = [str(num) for num in range(10)]
        special_symbols = ["+", "-", "_", "~", ".", "@"]
        all_letters = lowercase + uppercase + numbers + special_symbols

        if value:
            number_of_index = value.find("@")
            if number_of_index > 0 and value[number_of_index - 1] == "_":
                raise serializers.ValidationError("Invalid email")

            # check for length
            if len(value) < 6 or len(value) > 55:
                raise serializers.ValidationError("Invalid email")

            # check for allowed letters, numbers and special symbols
            for letter in value:
                if letter not in all_letters:
                    raise serializers.ValidationError("Invalid email")

            # check for last two characters
            if (value[-2] not in lowercase) or (value[-1] not in lowercase):
                raise serializers.ValidationError("Invalid email")

            # check for email prefix format
            prefix_letters = lowercase + uppercase + numbers
            underscore = value.find("_")
            dot = value.find(".")
            dash = value.find("-")

            if underscore >= 0 and value[underscore + 1] not in prefix_letters:
                raise serializers.ValidationError("Invalid email")

            if dot >= 0 and value[dot + 1] not in prefix_letters:
                raise serializers.ValidationError("Invalid email")

            if dash >= 0 and value[dash + 1] not in prefix_letters:
                raise serializers.ValidationError("Invalid email")

            # check for dot existance
            if "." not in value:
                raise serializers.ValidationError("Invalid email")

        return value

    def validate_passport_id(self, value: str) -> str:
        if value and not (
            value.isdigit() or (any(char.isdigit() for char in value) and any(char.isupper() for char in value))
        ):
            raise serializers.ValidationError("Invalid passport ID")
        return value

    def create(self, validated_data: dict) -> dict:
        validated_data.pop("password2", None)
        validated_data.pop("otp_code", None)
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        exclude = ("uuid", "last_login", "create_at", "is_active", "is_staff", "is_admin")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
            "otp_code": {"write_only": True},
        }


class UserRegistrationRequiredFieldsSerializer(UserRegistrationSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
        self.fields["otp_code"].required = False
