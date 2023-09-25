from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from auth_user.serializers.token_serializer import MyTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(
    tags=["Auth"],
)
class MyTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    tags=["Auth"],
)
class MyTokenBlacklistView(TokenBlacklistView):
    pass
