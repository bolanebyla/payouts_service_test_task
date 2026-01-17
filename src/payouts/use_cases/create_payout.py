from django.db.transaction import atomic

from payouts.dtos import CreatePayoutDto
from payouts.interfaces import PayoutMessagePublisher
from payouts.models import Payout, PayoutsStatuses
from payouts.repositories.payouts_repo import PayoutsRepo


class CreatePayoutUseCase:
    """Создание заявки на выплату средств"""

    def __init__(self, payouts_repo: PayoutsRepo, payout_message_publisher: PayoutMessagePublisher):
        self._payouts_repo = payouts_repo
        self._payout_message_publisher = payout_message_publisher

    @atomic
    def execute(self, create_dto: CreatePayoutDto) -> None:
        payout = Payout(
            amount=create_dto.amount,
            currency=create_dto.currency,
            recipient_details=create_dto.recipient_details,
            status=PayoutsStatuses.NEW,
            comment=create_dto.comment,
        )

        self._payouts_repo.save(payout=payout)

        self._payout_message_publisher.send_to_process_payout(payout_id=payout.id)
