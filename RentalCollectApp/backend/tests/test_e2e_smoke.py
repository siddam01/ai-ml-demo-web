import time
from datetime import date

BASE = "/api/v1"


def _unique_mobile() -> str:
    # 10 digits to satisfy validation. Not real phone.
    return str(int(time.time()))[-10:]


async def test_register_login_and_crud_smoke(client) -> None:
    mobile = _unique_mobile()

    # Register
    r = await client.post(
        f"{BASE}/auth/register",
        json={"name": "Test Owner", "mobile": mobile, "password": "password123"},
    )
    assert r.status_code in (201, 409), r.text  # 409 if re-run quickly with same mobile

    # Login (OAuth2PasswordRequestForm)
    r = await client.post(
        f"{BASE}/auth/login",
        data={"username": mobile, "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    tokens = r.json()
    assert "access_token" in tokens and "refresh_token" in tokens
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # Create property
    r = await client.post(
        f"{BASE}/properties",
        json={"property_name": "Test Property", "address": "Somewhere"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    prop = r.json()

    # Create unit
    r = await client.post(
        f"{BASE}/properties/{prop['id']}/units",
        json={"unit_name": "A-101", "rent_amount": "5000.00"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    unit = r.json()

    # Create tenant
    r = await client.post(
        f"{BASE}/tenants",
        json={"unit_id": unit["id"], "tenant_name": "Tenant One", "mobile": _unique_mobile(), "deposit": "0"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    tenant = r.json()

    # Create payment
    r = await client.post(
        f"{BASE}/payments",
        json={
            "tenant_id": tenant["id"],
            "amount": "5000.00",
            "payment_date": str(date.today()),
            "status": "paid",
            "note": "test",
        },
        headers=headers,
    )
    assert r.status_code == 201, r.text

    # Report
    r = await client.get(f"{BASE}/reports/pending-dues", params={"as_of": str(date.today())}, headers=headers)
    assert r.status_code == 200, r.text

