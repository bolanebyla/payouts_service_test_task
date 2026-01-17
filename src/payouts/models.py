from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PayoutsStatuses(models.TextChoices):
    """Статусы заявок на выплату средств"""

    NEW = "NEW", "Новая"
    PROCESSING = "PROCESSING", "Обработка заявки"
    COMPLETED = "COMPLETED", "Заявка обработана"
    FAILED = "FAILED", "Ошибка обработки"
    CANCELLED = "CANCELLED", "Отменена"


class PayoutsCurrencies(models.TextChoices):
    """Возможные валюты заявок на выплату средств"""

    RUB = "RUB", "Российский рубль"
    USD = "USD", "Доллар США"
    EUR = "EUR", "Евро"


class Payout(models.Model):
    """Заявка на выплату средств"""

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=18,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Сумма выплаты",
        db_comment="Сумма выплаты",
    )

    currency = models.TextField(
        choices=PayoutsCurrencies.choices,
        verbose_name="Валюта",
        db_comment="Валюта",
    )

    recipient_details = models.TextField(
        verbose_name="Реквизиты получателя",
        db_comment="Реквизиты получателя",
    )
    status = models.TextField(
        choices=PayoutsStatuses.choices,
        default=PayoutsStatuses.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.CharField(
        null=True,
        default=None,
        max_length=1000,
        verbose_name="Комментарий",
        db_comment="Комментарий",
    )

    class Meta:
        db_table = "payouts"
        db_table_comment = "Заявки на выплату"
