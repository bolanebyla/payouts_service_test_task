from rest_framework import routers

from payouts.api.views import PayoutsViewSet

payouts_api_router = routers.SimpleRouter()

payouts_api_router.register("", PayoutsViewSet)
