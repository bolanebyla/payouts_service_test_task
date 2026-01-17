import logging
import time

from django.db.transaction import atomic

from payouts.models import PayoutsStatuses
from payouts.repositories.payouts_repo import PayoutsRepo


class ProcessNewPayoutUseCase:
    """Обработка новой заявки на выплату"""

    def __init__(self, payouts_repo: PayoutsRepo):
        self._payouts_repo = payouts_repo

        self.logger = logging.getLogger(ProcessNewPayoutUseCase.__name__)

    def execute(self, payout_id: int) -> None:
        with atomic():
            payout = self._payouts_repo.get_by_id_with_lock(payout_id=payout_id)

            if payout.status != PayoutsStatuses.NEW:
                self.logger.warning(
                    'Обработка заявки на выплату с id "%s" не запущена, '
                    'так как заявка находится в статусе "%s"',
                    payout_id,
                    payout.status,
                )
                return

            payout.status = PayoutsStatuses.PROCESSING
            self._payouts_repo.save(payout)

        self.logger.info('Обработка заявки на выплату с id "%s" запущена', payout_id)
        # имитация продолжительной работы
        time.sleep(3)

        with atomic():
            payout = self._payouts_repo.get_by_id_with_lock(payout_id=payout_id)
            if payout.status != PayoutsStatuses.PROCESSING:
                self.logger.warning(
                    'Обработка заявки на выплату с id "%s" прервана, '
                    'так как заявка находится в статусе "%s"',
                    payout_id,
                    payout.status,
                )
                return

            payout.status = PayoutsStatuses.COMPLETED
            self._payouts_repo.save(payout)

        self.logger.info('Обработка заявки на выплату с id "%s" завершена', payout_id)
