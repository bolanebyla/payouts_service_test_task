from celery import shared_task
from django.db import DatabaseError, OperationalError


@shared_task(
    autoretry_for=(DatabaseError, OperationalError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=5,
)
def process_payout_task(
    payout_id: int,
) -> None:
    from payouts.deps import create_process_new_payout_use_case

    use_case = create_process_new_payout_use_case()
    use_case.execute(payout_id=payout_id)
