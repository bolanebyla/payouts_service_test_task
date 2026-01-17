from payouts.models import Payout


class PayoutsRepo:
    """Репозиторий для заявок на выплату"""

    def save(self, payout: Payout):
        payout.save()

    def get_by_id_with_lock(self, payout_id: int) -> Payout:
        return Payout.objects.select_for_update().get(id=payout_id)
