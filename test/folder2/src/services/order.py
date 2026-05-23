class OrderService:
    def create_order(self, item, qty, discount=0):
        total = qty * 10 * (1 - discount)
        return {"item": item, "qty": qty, "total": total, "status": "pending"}

    def cancel_order(self, id):
        return {"id": id, "status": "cancelled"}
