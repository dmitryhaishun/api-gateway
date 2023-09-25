from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # apps
    path("api/accounts/", include("account.urls")),
    path("api/user/", include("user.urls")),
    path("api/cards/", include("card.urls")),
    # path("api/deposit/", include("deposit.urls")),
    path("api/loans/", include("loan.urls")),
    path("api/auth/", include("auth_user.urls")),
    # auth
    path('api-auth/', include('rest_framework.urls')),
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),
    # Swagger
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
