from unittest.mock import MagicMock, create_autospec

import pytest
from rest_framework.test import APIClient

from payouts.use_cases import CreatePayoutUseCase


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="function")
def create_payout_use_case() -> MagicMock:
    return create_autospec(CreatePayoutUseCase, spec_set=True, instance=True)
