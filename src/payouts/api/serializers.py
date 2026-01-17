from typing import ClassVar

from rest_framework import serializers

from payouts.models import Payout


class PayoutCreateSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для создания заявки на выплату"""

    class Meta:
        model = Payout
        fields: ClassVar = [
            "amount",
            "currency",
            "recipient_details",
            "comment",
        ]


class PayoutUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для обновления заявки на выплату"""

    class Meta:
        model = Payout
        fields: ClassVar = [
            "status",
            "comment",
        ]


class PayoutReadSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для чтения заявки на выплату"""

    class Meta:
        model = Payout
        fields: ClassVar = [
            "id",
            "amount",
            "currency",
            "recipient_details",
            "status",
            "created_at",
            "updated_at",
            "comment",
        ]
