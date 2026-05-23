def test_order_create():
    svc = OrderService()
    result = svc.create_order("apple", 3)
    assert result["status"] == "pending"
