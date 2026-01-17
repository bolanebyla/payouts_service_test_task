from payouts.interfaces import PayoutMessagePublisher
from payouts.tasks import process_payout_task


class PayoutMessagePublisherImpl(PayoutMessagePublisher):
    def send_to_process_payout(self, payout_id: int) -> None:
        process_payout_task.delay_on_commit(payout_id=payout_id)
