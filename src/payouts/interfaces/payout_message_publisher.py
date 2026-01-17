from abc import ABC, abstractmethod


class PayoutMessagePublisher(ABC):
    """Паблишер сообщений для заявок на выплаты"""

    @abstractmethod
    def send_to_process_payout(self, payout_id: int) -> None:
        """Отправить сообщение на обработку заявки на выплату"""
        ...
