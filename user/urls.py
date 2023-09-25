from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views.user_info import UserInfo
from user.views.views import UserAPI, Example

router = DefaultRouter()
router.register(r'example', Example, basename='example')
router.register(r'info', UserInfo, basename='info')


urlpatterns = [
    path("", UserAPI.as_view()),
]

urlpatterns.extend(router.urls)
