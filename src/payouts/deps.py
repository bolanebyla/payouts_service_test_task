from payouts.interfaces import PayoutMessagePublisher
from payouts.publishers import PayoutMessagePublisherImpl
from payouts.repositories.payouts_repo import PayoutsRepo
from payouts.use_cases import CreatePayoutUseCase, ProcessNewPayoutUseCase


def create_payouts_repo() -> PayoutsRepo:
    return PayoutsRepo()


def create_payout_message_publisher() -> PayoutMessagePublisher:
    return PayoutMessagePublisherImpl()


def create_process_new_payout_use_case() -> ProcessNewPayoutUseCase:
    return ProcessNewPayoutUseCase(
        payouts_repo=create_payouts_repo(),
    )


def create_create_payout_use_case() -> CreatePayoutUseCase:
    return CreatePayoutUseCase(
        payouts_repo=create_payouts_repo(),
        payout_message_publisher=create_payout_message_publisher(),
    )
