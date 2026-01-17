from typing import ClassVar

from rest_framework.viewsets import ModelViewSet

from payouts.api.serializers import (
    PayoutCreateSerializer,
    PayoutReadSerializer,
    PayoutUpdateSerializer,
)
from payouts.deps import create_create_payout_use_case
from payouts.dtos import CreatePayoutDto
from payouts.models import Payout


class PayoutsViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]  # noqa: RUF012
    queryset = Payout.objects.all().order_by("-id")

    serializer_action_classes: ClassVar = {
        "create": PayoutCreateSerializer,
        "partial_update": PayoutUpdateSerializer,
    }
    serializer_class = PayoutReadSerializer

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, self.serializer_class)

    def perform_create(self, serializer: PayoutCreateSerializer):
        use_case = create_create_payout_use_case()

        validated_data = serializer.validated_data
        create_dto = CreatePayoutDto(**validated_data)
        use_case.execute(create_dto=create_dto)
