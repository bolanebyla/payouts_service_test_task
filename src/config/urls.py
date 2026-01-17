from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from payouts.api.urls import payouts_api_router

schema_view = get_schema_view(
    openapi.Info(
        title="Payouts service",
        default_version="v1",
        description="Сервис для управления заявками на выплату средств",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("schema-swagger-ui"), permanent=False)),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/payouts/", include(payouts_api_router.urls)),
]
