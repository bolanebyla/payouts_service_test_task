from celery import shared_task


@shared_task
def process_payout_task(
    payout_id: int,
) -> None:
    from payouts.deps import create_process_new_payout_use_case

    use_case = create_process_new_payout_use_case()
    use_case.execute(payout_id=payout_id)
