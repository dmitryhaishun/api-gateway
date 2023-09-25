from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'registration', views.RegistrationViewSet, basename='register')
router.register(r'registration/final', views.FinalRegistrationViewSet, basename='final_register')


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.MyTokenBlacklistView.as_view(), name='logout'),
]

urlpatterns.extend(router.urls)
