from unittest.mock import MagicMock, create_autospec

import pytest

from payouts.interfaces import PayoutMessagePublisher
from payouts.repositories.payouts_repo import PayoutsRepo


@pytest.fixture(scope="function")
def payouts_repo() -> MagicMock:
    return create_autospec(PayoutsRepo, spec_set=True, instance=True)


@pytest.fixture(scope="function")
def payout_message_publisher() -> MagicMock:
    return create_autospec(PayoutMessagePublisher, spec_set=True, instance=True)
