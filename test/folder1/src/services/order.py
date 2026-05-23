class OrderService:
    def create_order(self, item, qty):
        return {"item": item, "qty": qty, "status": "pending"}

    def cancel_order(self, id):
        return {"id": id, "status": "cancelled"}
