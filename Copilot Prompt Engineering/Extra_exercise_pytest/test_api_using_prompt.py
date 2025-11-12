import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from app import app, ETAG  # Adjust import if your file name differs

AUTH_HEADER = {"Authorization": "Bearer demo-token"}
WRONG_AUTH_HEADER = {"Authorization": "Bearer wrong-token"}

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

def create_order(client, payload):
    return client.post("/orders", json=payload, headers=AUTH_HEADER)

# -------------------------------
# 1. Happy path: create and retrieve
# -------------------------------
def test_create_and_get_order(client):
    payload = {"user_id": "user123", "amount": 100.50, "currency": "USD"}
    resp = create_order(client, payload)
    assert resp.status_code == 201
    data = resp.json()
    assert set(data.keys()) == {"id", "status", "user_id", "amount", "currency"}
    assert Decimal(data["amount"]) == Decimal("100.50")
    oid = data["id"]

    # Retrieve
    get_resp = client.get(f"/orders/{oid}", headers=AUTH_HEADER)
    assert get_resp.status_code == 200
    assert get_resp.json() == data

# -------------------------------
# 2. Authorization failures
# -------------------------------
@pytest.mark.parametrize("headers", [
    {},  # Missing
    {"Authorization": ""},  # Empty
    WRONG_AUTH_HEADER,  # Wrong token
])
def test_auth_failures(client, headers):
    payload = {"user_id": "user123", "amount": 10.00, "currency": "USD"}
    resp = client.post("/orders", json=payload, headers=headers)
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unauthorized"

# -------------------------------
# 3. Pagination behavior
# -------------------------------
def test_pagination(client):
    # Create 60 orders
    for i in range(60):
        create_order(client, {"user_id": f"user{i}", "amount": 10.00, "currency": "USD"})

    # Default limit=10
    resp = client.get("/orders", headers=AUTH_HEADER)
    assert resp.status_code == 200
    assert len(resp.json()) == 10

    # Custom limit within cap
    resp = client.get("/orders?limit=20", headers=AUTH_HEADER)
    assert len(resp.json()) == 20

    # Limit beyond cap (should cap at 50)
    resp = client.get("/orders?limit=100", headers=AUTH_HEADER)
    assert len(resp.json()) == 50

    # Offset works
    resp = client.get("/orders?limit=10&offset=50", headers=AUTH_HEADER)
    assert len(resp.json()) == 10

# -------------------------------
# 4. PUT requires correct ETag
# -------------------------------
def test_put_etag_behavior(client):
    payload = {"user_id": "etaguser", "amount": 20.00, "currency": "USD"}
    create_resp = create_order(client, payload)
    oid = create_resp.json()["id"]

    # Get current ETag from app state
    correct_etag = ETAG[oid]

    update_payload = {"user_id": "etaguser", "amount": 30.00, "currency": "USD"}

    # Missing ETag
    resp_missing = client.put(f"/orders/{oid}", json=update_payload, headers=AUTH_HEADER)
    assert resp_missing.status_code == 412

    # Wrong ETag
    resp_wrong = client.put(f"/orders/{oid}", json=update_payload,
                            headers={**AUTH_HEADER, "If-Match": "wrong"})
    assert resp_wrong.status_code == 412

    # Correct ETag
    resp_ok = client.put(f"/orders/{oid}", json=update_payload,
                         headers={**AUTH_HEADER, "If-Match": correct_etag})
    assert resp_ok.status_code == 200
    assert Decimal(resp_ok.json()["amount"]) == Decimal("30.00")

# -------------------------------
# 5. Validation errors
# -------------------------------
@pytest.mark.parametrize("payload,expected_field", [
    ({"user_id": "", "amount": 10.00, "currency": "USD"}, "user_id"),
    ({"user_id": "u", "amount": -5.00, "currency": "USD"}, "amount"),
    ({"user_id": "u", "amount": 10.00, "currency": "usd"}, "currency"),
])
def test_validation_errors(client, payload, expected_field):
    resp = client.post("/orders", json=payload, headers=AUTH_HEADER)
    assert resp.status_code == 422
    # Check that the error mentions the expected field
    assert any(expected_field in str(err["loc"]) for err in resp.json()["detail"])