from dataclasses import dataclass
from decimal import Decimal


@dataclass(kw_only=True, frozen=True, slots=True)
class CreatePayoutDto:
    """Dto для создания заявки на выплату средств"""

    amount: Decimal
    currency: str
    recipient_details: str
    comment: str | None = None
