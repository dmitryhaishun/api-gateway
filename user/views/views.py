from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers.user_serializer import AllUsers, UserSerializer


@extend_schema(
    tags=["Example"],
)
class UserAPI(APIView):
    def get(self, request: Request) -> Response:
        data = {"message": "Hello, User!"}
        serializer = UserSerializer(data)
        return Response(serializer.data)


@extend_schema(
    tags=["Example"],
)
class Example(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AllUsers
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
