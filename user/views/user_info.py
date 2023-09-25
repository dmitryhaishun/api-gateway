from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers.user_serializer import UserInfoSerializer


@extend_schema(
    tags=["User"],
)
class UserInfo(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> dict:
        user = self.request.user
        queryset = User.objects.filter(id=user.id).first()
        return queryset

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        if queryset is not None:
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        else:
            return Response({"detail": "User not found."}, status=404)
