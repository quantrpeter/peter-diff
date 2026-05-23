def test_e2e_flow():
    resp = client.post("/order", json={"item": "apple", "qty": 2})
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"
