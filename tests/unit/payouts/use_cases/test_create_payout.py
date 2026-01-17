from decimal import Decimal

import pytest

from payouts.dtos import CreatePayoutDto
from payouts.interfaces import PayoutMessagePublisher
from payouts.models import PayoutsStatuses
from payouts.repositories.payouts_repo import PayoutsRepo
from payouts.use_cases import CreatePayoutUseCase


@pytest.fixture
def use_case(
    payouts_repo: PayoutsRepo,
    payout_message_publisher: PayoutMessagePublisher,
) -> CreatePayoutUseCase:
    return CreatePayoutUseCase(
        payouts_repo=payouts_repo,
        payout_message_publisher=payout_message_publisher,
    )


@pytest.mark.django_db
def test__create_payout_use_case_success_creates_payout_and_publishes(
    use_case: CreatePayoutUseCase,
    payouts_repo: PayoutsRepo,
    payout_message_publisher: PayoutMessagePublisher,
) -> None:
    dto = CreatePayoutDto(
        amount=Decimal("10000.50"),
        currency="RUB",
        recipient_details="123454321",
        comment="test comment",
    )

    def save_side_effect(*, payout):
        payout.id = 123

    payouts_repo.save.side_effect = save_side_effect

    use_case.execute(dto)

    payouts_repo.save.assert_called_once()
    saved_payout = payouts_repo.save.call_args.kwargs["payout"]

    assert saved_payout.amount == Decimal("10000.50")
    assert saved_payout.currency == "RUB"
    assert saved_payout.recipient_details == "123454321"
    assert saved_payout.comment == "test comment"
    assert saved_payout.status == PayoutsStatuses.NEW

    payout_message_publisher.send_to_process_payout.assert_called_once_with(payout_id=123)
