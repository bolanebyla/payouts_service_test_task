from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from payouts.use_cases import CreatePayoutUseCase


def test__payouts_create__success(
    api_client: APIClient,
    create_payout_use_case: CreatePayoutUseCase,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        "payouts.api.views.create_create_payout_use_case",
        lambda: create_payout_use_case,
    )

    url = reverse("payout-list")
    payload = {
        "amount": "10000.50",
        "currency": "RUB",
        "recipient_details": "123454321",
        "comment": "test comment",
    }

    resp = api_client.post(url, data=payload, format="json")

    assert resp.status_code == 201, resp.data

    create_payout_use_case.execute.assert_called_once()
    dto = create_payout_use_case.execute.call_args.kwargs["create_dto"]

    assert dto.amount == Decimal("10000.50")
    assert dto.currency == "RUB"
    assert dto.recipient_details == "123454321"
    assert dto.comment == "test comment"


def test__payouts_create__negative_amount(
    api_client: APIClient,
    create_payout_use_case: CreatePayoutUseCase,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        "payouts.api.views.create_create_payout_use_case",
        lambda: create_payout_use_case,
    )

    url = reverse("payout-list")
    payload = {
        "amount": "-1.00",
        "currency": "RUB",
        "recipient_details": "123454321",
        "comment": "test comment",
    }

    resp = api_client.post(url, data=payload, format="json")

    assert resp.status_code == 400, resp.data
    assert "amount" in resp.data

    create_payout_use_case.execute.assert_not_called()


def test__payouts_create__invalid_currency(
    api_client: APIClient,
    create_payout_use_case: CreatePayoutUseCase,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        "payouts.api.views.create_create_payout_use_case",
        lambda: create_payout_use_case,
    )

    url = reverse("payout-list")
    payload = {
        "amount": "100.00",
        "currency": "ZZZ",
        "recipient_details": "123454321",
        "comment": "test comment",
    }

    resp = api_client.post(url, data=payload, format="json")

    assert resp.status_code == 400, resp.data
    assert "currency" in resp.data

    create_payout_use_case.execute.assert_not_called()


def test__payouts_create__comment_too_long(
    api_client: APIClient,
    create_payout_use_case: CreatePayoutUseCase,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(
        "payouts.api.views.create_create_payout_use_case",
        lambda: create_payout_use_case,
    )

    url = reverse("payout-list")
    payload = {
        "amount": "100.00",
        "currency": "RUB",
        "recipient_details": "123454321",
        "comment": "a" * 1001,
    }

    resp = api_client.post(url, data=payload, format="json")

    assert resp.status_code == 400, resp.data
    assert "comment" in resp.data

    create_payout_use_case.execute.assert_not_called()
