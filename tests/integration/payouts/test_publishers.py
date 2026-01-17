from unittest.mock import patch

from payouts.publishers import PayoutMessagePublisherImpl


@patch("payouts.publishers.process_payout_task.delay_on_commit")
def test__payout_message_publisher__calls_celery_task(
    mock_delay_on_commit,
):
    publisher = PayoutMessagePublisherImpl()
    payout_id = 123

    publisher.send_to_process_payout(payout_id=payout_id)

    mock_delay_on_commit.assert_called_once_with(payout_id=payout_id)
